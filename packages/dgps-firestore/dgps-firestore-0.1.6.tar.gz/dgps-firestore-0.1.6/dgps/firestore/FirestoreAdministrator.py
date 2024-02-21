# @TODO: add update time to firstore
# @TODO: add update time when incrementing firestore

import datetime
import logging
import pprint
import re
import traceback
import uuid

import pytz
from google.cloud import firestore
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class DocumentNotFoundError(Exception):
    pass


class FirestoreAdminError(Exception):
    pass


# @TODO: chatGPT recommends to use a status handler...
# class StatusHandler:
#     def __init__(self):
#         self.messages = []

#     def add_status(self, message):
#         self.messages.append(message)

#     def get_statuses(self):
#         return self.messages


class FirestoreAdministrator:
    def __init__(self, singleton=False):
        # self.db = firestore.AsyncClient()
        self.db = firestore.Client()
        self._is_singleton = singleton

    @staticmethod
    def update_status(status, msg):
        if status is not None:
            status.append(msg)
        else:
            status = [msg]
        LOG.info(msg)
        return status

    def update_fields(self, collection_id, document_id, update_dict):
        status = []

        def key_transform(key):
            return re.sub(r"[^\w.]+", "", key)

        try:
            ref = self.db.collection(str(collection_id)).document(str(document_id))
            doc = ref.get()
            doc_exists = doc.exists

            for key, _ in update_dict.items():
                new_key = key_transform(key)
                if new_key != key:
                    status = self.update_status(status, f"renaming {key} to {new_key}")

            firestore_update_dict = {
                key_transform(key): value for key, value in update_dict.items()
            }

            # Set modification timestamp
            firestore_update_dict["last_update"] = firestore.SERVER_TIMESTAMP
            firestore_update_dict[
                "firestore_modification_timestamp"
            ] = firestore.SERVER_TIMESTAMP

            # Set creation timestamp only if document does not exist
            if not doc_exists:
                firestore_update_dict[
                    "firestore_creation_timestamp"
                ] = firestore.SERVER_TIMESTAMP
                result = ref.set(firestore_update_dict, merge=True)
                status = self.update_status(
                    status,
                    f"created {firestore_update_dict} and updated timestamps in "
                    f"{collection_id} {document_id}",
                )
                return result
            result = ref.update(firestore_update_dict)
            status = self.update_status(
                status,
                f"updated {firestore_update_dict} and updated timestamps in "
                f"{collection_id} {document_id}",
            )
            return result
        except Exception as exc:
            error_text = (
                "Exception while updating firestore field.\n"
                f"collection: {collection_id}\n"
                f"document: {document_id}\n"
                f"increment_dict: {firestore_update_dict}\n"
                f"Stacktrace:\n{traceback.format_exc()}\n"
                f"Exception: {exc}"
            )
            LOG.error(error_text)
            raise FirestoreAdminError(error_text)

    def increment_field(self, collection_id, document_id, increment_dict):
        status = []

        def key_transform(key):
            return re.sub(r"[^\w.]+", "", key)

        try:
            ref = self.db.collection(str(collection_id)).document(str(document_id))
            doc = ref.get()
            doc_exists = doc.exists

            for key, _ in increment_dict.items():
                new_key = key_transform(key)
                if new_key != key:
                    status = self.update_status(status, f"renaming {key} to {new_key}")

            firestore_increment_dict = {
                key_transform(key): firestore.Increment(value)
                for key, value in increment_dict.items()
            }

            # Set modification timestamp
            firestore_increment_dict["last_update"] = firestore.SERVER_TIMESTAMP
            firestore_increment_dict[
                "firestore_modification_timestamp"
            ] = firestore.SERVER_TIMESTAMP

            # Set creation timestamp only if document does not exist
            if not doc_exists:
                firestore_increment_dict[
                    "firestore_creation_timestamp"
                ] = firestore.SERVER_TIMESTAMP
            result = ref.update(firestore_increment_dict)
            status = self.update_status(
                status,
                f"incremented {firestore_increment_dict} and updated timestamps in "
                f"{collection_id} {document_id}",
            )
            return result

        except Exception as exc:
            error_text = (
                "Exception while incrementing firestore field.\n"
                f"collection: {collection_id}\n"
                f"document: {document_id}\n"
                f"increment_dict: {increment_dict}\n"
                f"Stacktrace:\n{traceback.format_exc()}\n"
                f"Exception: {exc}"
            )
            LOG.error(error_text)
            raise FirestoreAdminError(error_text)

    def add_document_to_collection(self, collection_id, document_id, data):
        status = []
        print("add_document_to_collection")
        print(isinstance(data, BaseModel))
        if isinstance(data, BaseModel):
            firestore_data = data.model_dump(
                exclude_defaults=True,
                exclude_none=True,
            )
        else:
            firestore_data = data.copy()
        print(data)
        try:
            doc_ref = self.db.collection(str(collection_id)).document(str(document_id))
            firestore_data["firestore_creation_timestamp"] = firestore.SERVER_TIMESTAMP
            firestore_data[
                "firestore_modification_timestamp"
            ] = firestore.SERVER_TIMESTAMP
            result = doc_ref.set(firestore_data, merge=True)
            status = self.update_status(
                status,
                f"Added {document_id} document to {collection_id} firestore collection.",
            )
            return result
        except Exception as exc:
            error_text = (
                "Exception while while writing to firestore.\n"
                f"collection: {collection_id}\n"
                f"document: {document_id}\n"
                f"data: {data}\n"
                f"Stacktrace:\n{traceback.format_exc()}\n"
                f"Exception: {exc}"
            )
            LOG.error(error_text)
            raise FirestoreAdminError(error_text)

    # def get_firebase_doc_dict(self, collection_id, document_id):
    #     collection_ref = self.db.collection(str(collection_id))
    #     doc_ref = collection_ref.document(str(document_id))
    #     doc = doc_ref.get()
    #     if doc.exists:
    #         return doc.to_dict()
    #     else:
    #         return None

    def delete_document_from_collection(
        self, collection_id, document_id, delete_subcollections=False
    ):
        LOG.info("delete_document_from_collection")
        status = []
        try:
            doc_ref = self.db.collection(str(collection_id)).document(str(document_id))
            doc = doc_ref.get()
            if doc.exists:
                status = self.update_status(status, f"Document {document_id} exists.")
                LOG.info(f"Document {document_id} exists in {collection_id}.")
                LOG.info(f"Deleting {document_id} from {collection_id}.")
                LOG.info(f"Document data: \n{pprint.pformat(doc.to_dict())}")
                sub_collections = doc_ref.collections()
                has_subcollections = False
                for _ in sub_collections:
                    has_subcollections = True
                    break  # Exit after finding the first subcollection
                if has_subcollections:
                    LOG.info("There are subcollections.")
                    status = self.update_status(
                        status, f"Document {document_id} has subcollections."
                    )
                    if not delete_subcollections:
                        raise ValueError(
                            "There are subcollections. Set delete_subcollections=True to delete them."
                        )
                    else:
                        raise ValueError("Subcollection deletion is not implemented.")
                # if delete_subcollections:
                #     for sub_collection in sub_collections:
                #         sub_collection_id = sub_collection.id
                #         sub_collection_ref = doc_ref.collection(sub_collection_id)
                #         sub_docs = sub_collection_ref.stream()
                #         for sub_doc in sub_docs:
                #             sub_doc_id = sub_doc.id
                #             sub_doc_ref = sub_collection_ref.document(sub_doc_id)
                #             sub_doc_ref.delete()
                #             status = self.update_status(
                #                 status,
                #                 f"Deleted {sub_doc_id} document from {sub_collection_id} firestore subcollection.",
                #             )

                result = doc_ref.delete()
                status = self.update_status(
                    status,
                    f"Deleted {document_id} document from {collection_id} firestore collection.",
                )
                return result
            else:
                status = self.update_status(
                    status, f"Document {document_id} does not exist."
                )
                raise DocumentNotFoundError(
                    f"Document {document_id} does not exist in {collection_id} firestore collection."
                )
        except DocumentNotFoundError as exc:
            LOG.error(exc)
            raise exc
        except Exception as exc:
            error_text = (
                "Exception while attempting to delete from firestore.\n"
                f"collection: {collection_id}\n"
                f"document: {document_id}\n"
                f"Stacktrace:\n{traceback.format_exc()}\n"
                f"Exception: {exc}"
            )
            LOG.error(error_text)
            status = self.update_status(status, error_text)

    def update_document_in_collection(self, collection_id, document_id, data):
        status = []
        results = []
        firestore_data = data.copy()
        try:
            current_datetime = datetime.datetime.now(pytz.utc)
            current_datestamp = current_datetime.strftime("%Y-%m-%d_%H:%M:%S_%Z%z")
            uuid4 = str(uuid.uuid4())
            doc_dict = self.get_firebase_doc_dict(collection_id, document_id)
            if doc_dict is not None:
                status = self.update_status(status, f"Document {document_id} exists.")
                new_collection_id = collection_id + "_archive"
                new_document_id = (
                    document_id + "_" + current_datestamp + "_" + str(uuid4)
                )
                results.append(
                    self.add_document_to_collection(
                        new_collection_id, new_document_id, doc_dict
                    )
                )
            results.append(
                self.add_document_to_collection(
                    collection_id, document_id, firestore_data
                )
            )
            status = self.update_status(
                status,
                f"Updated {document_id} document in {collection_id} firestore collection.",
            )
            return results
        except Exception as exc:
            error_text = (
                "Exception while writing to firestore.\n"
                f"collection: {collection_id}\n"
                f"document: {document_id}\n"
                f"data: {firestore_data}\n"
                f"Stacktrace:\n{traceback.format_exc()}\n"
                f"Exception: {exc}"
            )
            LOG.error(error_text)
            raise FirestoreAdminError(error_text)

    def document_exists(self, collection_id, document_id):
        doc_ref = self.db.collection(str(collection_id)).document(str(document_id))
        return doc_ref.get().exists

    def query_firebase(self, collection_id, document_id, query):
        doc_dict = self.get_firebase_doc_dict(collection_id, document_id)
        if doc_dict is not None:
            return doc_dict[query]
        else:
            return None

    # def get_firebase_docs(self, collection_id):
    #     collection_ref = self.db.collection(str(collection_id))
    #     docs_ref = collection_ref.stream()

    #     for doc in docs_ref:
    #         print(f'{doc.id} => {doc.to_dict()}')

    def get_firebase_doc_dict(self, collection_id, document_id):
        collection_ref = self.db.collection(str(collection_id))
        doc_ref = collection_ref.document(str(document_id))
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def list_collections(self):
        return [col.id for col in self.db.collections()]


_singleton_instance = None


def get_firestore_administrator(singleton=True):
    global _singleton_instance
    if singleton:
        if _singleton_instance is None:
            _singleton_instance = FirestoreAdministrator(singleton=True)
        return _singleton_instance
    else:
        return FirestoreAdministrator(singleton=False)


if __name__ == "__main__":
    fs_admin_singleton = get_firestore_administrator()
    print(fs_admin_singleton.list_collections())


# Usage:
# # To get a singleton instance:
# fs_admin_singleton = get_firestore_administrator()

# # To get a new, non-singleton instance:
# fs_admin_non_singleton = get_firestore_administrator(singleton=False)

# # # Assume these functions are defined to convert your objects to and from dictionaries
# def object_to_dict(obj):
#     # Implement this function based on your object structure
#     return obj.model_dump(
#         exclude_defaults=True,
#         exclude_none=True,
#     )

# def dict_to_object(dict_obj, obj_class):
#     # Implement this function based on your object structure
#     return obj_class.load_from_model(dict_obj)

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# def get_object(obj_id, obj_class, collection_id):
#     doc_ref = db.collection(collection_id).document(obj_id)
#     doc_dict = doc_ref.get().to_dict()
#     return dict_to_object(doc_dict, obj_class)

# # Example Usage
# # Assume `voter` is an instance of Voter class
# save_object(voter, 'Voters')

# # To get the object back from Firestore
# retrieved_voter = get_object(voter.prefix + voter.id, Voter, 'Voters')
