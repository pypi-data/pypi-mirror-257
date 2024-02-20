from dataclasses import dataclass
from typing import Optional, List, Union, Literal




@dataclass
class KayocError:
    succes: bool
    message: str
    done: bool
    error: str

    @classmethod
    def from_json(cls, data: dict) -> "KayocError":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            error = data["error"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["error"] = self.error

        return data

@dataclass
class CreateDatabaseRequest:
    database_name: str

    @classmethod
    def from_json(cls, data: dict) -> "CreateDatabaseRequest":
        return cls(
            database_name = data["database_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name

        return data

@dataclass
class CreateDatabaseResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "CreateDatabaseResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteDatabaseRequest:
    database_name: str

    @classmethod
    def from_json(cls, data: dict) -> "DeleteDatabaseRequest":
        return cls(
            database_name = data["database_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name

        return data

@dataclass
class DeleteDatabaseResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteDatabaseResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DatabaseInfoRequest:
    database_name: str

    @classmethod
    def from_json(cls, data: dict) -> "DatabaseInfoRequest":
        return cls(
            database_name = data["database_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name

        return data

@dataclass
class UserDatabasePermissionInfo:
    user_id: int
    user_email: str
    database_id: int
    type: str

    @classmethod
    def from_json(cls, data: dict) -> "UserDatabasePermissionInfo":
        return cls(
            user_id = data["user_id"],
            user_email = data["user_email"],
            database_id = data["database_id"],
            type = data["type"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["user_id"] = self.user_id
        data["user_email"] = self.user_email
        data["database_id"] = self.database_id
        data["type"] = self.type

        return data

@dataclass
class DatabaseInfoItem:
    id: int
    name: str

    @classmethod
    def from_json(cls, data: dict) -> "DatabaseInfoItem":
        return cls(
            id = data["id"],
            name = data["name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name

        return data

@dataclass
class DateTime:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    @classmethod
    def from_json(cls, data: dict) -> "DateTime":
        return cls(
            year = data["year"],
            month = data["month"],
            day = data["day"],
            hour = data["hour"],
            minute = data["minute"],
            second = data["second"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["year"] = self.year
        data["month"] = self.month
        data["day"] = self.day
        data["hour"] = self.hour
        data["minute"] = self.minute
        data["second"] = self.second

        return data

@dataclass
class DatabaseInfoBuild:
    id: int
    name: str
    created_at: DateTime

    @classmethod
    def from_json(cls, data: dict) -> "DatabaseInfoBuild":
        return cls(
            id = data["id"],
            name = data["name"],
            created_at = DateTime.from_json(data['created_at']),
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["created_at"] = self.created_at.to_json()

        return data

@dataclass
class DatabaseInfoResponse:
    id: int
    name: str
    permissions: list[UserDatabasePermissionInfo]
    items: list[DatabaseInfoItem]
    builds: list[DatabaseInfoBuild]
    created_at: DateTime
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DatabaseInfoResponse":
        return cls(
            id = data["id"],
            name = data["name"],
            permissions = [UserDatabasePermissionInfo.from_json(item) for item in data["permissions"]],
            items = [DatabaseInfoItem.from_json(item) for item in data["items"]],
            builds = [DatabaseInfoBuild.from_json(item) for item in data["builds"]],
            created_at = DateTime.from_json(data['created_at']),
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["permissions"] = [UserDatabasePermissionInfo.to_json(item) for item in self.permissions]
        data["items"] = [DatabaseInfoItem.to_json(item) for item in self.items]
        data["builds"] = [DatabaseInfoBuild.to_json(item) for item in self.builds]
        data["created_at"] = self.created_at.to_json()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class RenameDatabaseRequest:
    database_name: str
    new_name: str

    @classmethod
    def from_json(cls, data: dict) -> "RenameDatabaseRequest":
        return cls(
            database_name = data["database_name"],
            new_name = data["new_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name
        data["new_name"] = self.new_name

        return data

@dataclass
class RenameDatabaseResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "RenameDatabaseResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class QuestionInfoRequest:
    question_id: int

    @classmethod
    def from_json(cls, data: dict) -> "QuestionInfoRequest":
        return cls(
            question_id = data["question_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["question_id"] = self.question_id

        return data

@dataclass
class AnswerInfo:
    content: str
    explanation: str
    rating: Optional[Literal["down", "neutral", "up"]]
    id: int

    @classmethod
    def from_json(cls, data: dict) -> "AnswerInfo":
        return cls(
            content = data["content"],
            explanation = data["explanation"],
            rating = data["rating"] if "rating" in data else None,
            id = data["id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["content"] = self.content
        data["explanation"] = self.explanation
        
        if self.rating is not None:
            data["rating"] = self.rating

        data["id"] = self.id

        return data

@dataclass
class MessageInfo:
    relevant_parts: list[int]
    answer: AnswerInfo
    content: str
    created_at: DateTime
    id: int

    @classmethod
    def from_json(cls, data: dict) -> "MessageInfo":
        return cls(
            relevant_parts = data["relevant_parts"],
            answer = AnswerInfo.from_json(data['answer']),
            content = data["content"],
            created_at = DateTime.from_json(data['created_at']),
            id = data["id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["relevant_parts"] = self.relevant_parts
        data["answer"] = self.answer.to_json()
        data["content"] = self.content
        data["created_at"] = self.created_at.to_json()
        data["id"] = self.id

        return data

@dataclass
class QuestionInfoResponse:
    succes: bool
    message: str
    done: bool
    created_at: DateTime
    messages: list[MessageInfo]

    @classmethod
    def from_json(cls, data: dict) -> "QuestionInfoResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            created_at = DateTime.from_json(data['created_at']),
            messages = [MessageInfo.from_json(item) for item in data["messages"]],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["created_at"] = self.created_at.to_json()
        data["messages"] = [MessageInfo.to_json(item) for item in self.messages]

        return data

@dataclass
class CreateAnswerRequest:
    question: str
    database_name: str
    keywords: Optional[list[str]]
    question_id: Optional[int]
    build_name: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "CreateAnswerRequest":
        return cls(
            question = data["question"],
            database_name = data["database_name"],
            keywords = data["keywords"] if "keywords" in data else None,
            question_id = data["question_id"] if "question_id" in data else None,
            build_name = data["build_name"] if "build_name" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        data["question"] = self.question
        data["database_name"] = self.database_name
        
        if self.keywords is not None:
            data["keywords"] = self.keywords

        
        if self.question_id is not None:
            data["question_id"] = self.question_id

        
        if self.build_name is not None:
            data["build_name"] = self.build_name


        return data

@dataclass
class CreateAnswerResponse:
    succes: bool
    message: str
    done: bool
    answer: str
    explanation: str
    context: str
    question_id: int

    @classmethod
    def from_json(cls, data: dict) -> "CreateAnswerResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            answer = data["answer"],
            explanation = data["explanation"],
            context = data["context"],
            question_id = data["question_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["answer"] = self.answer
        data["explanation"] = self.explanation
        data["context"] = self.context
        data["question_id"] = self.question_id

        return data

@dataclass
class CreateAnswerUpdateResponse:
    task: str
    total: Optional[int]
    count: Optional[int]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "CreateAnswerUpdateResponse":
        return cls(
            task = data["task"],
            total = data["total"] if "total" in data else None,
            count = data["count"] if "count" in data else None,
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["task"] = self.task
        
        if self.total is not None:
            data["total"] = self.total

        
        if self.count is not None:
            data["count"] = self.count

        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class AnswerInfoRequest:
    answer_id: int

    @classmethod
    def from_json(cls, data: dict) -> "AnswerInfoRequest":
        return cls(
            answer_id = data["answer_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["answer_id"] = self.answer_id

        return data

@dataclass
class RelevantPart:
    id: int
    content: str

    @classmethod
    def from_json(cls, data: dict) -> "RelevantPart":
        return cls(
            id = data["id"],
            content = data["content"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["content"] = self.content

        return data

@dataclass
class AnswerInfoResponse:
    answer: str
    question: str
    context: str
    explanation: str
    rating: Optional[Literal["down", "neutral", "up"]]
    question_id: int
    relevant_parts: list[RelevantPart]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "AnswerInfoResponse":
        return cls(
            answer = data["answer"],
            question = data["question"],
            context = data["context"],
            explanation = data["explanation"],
            rating = data["rating"] if "rating" in data else None,
            question_id = data["question_id"],
            relevant_parts = [RelevantPart.from_json(item) for item in data["relevant_parts"]],
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["answer"] = self.answer
        data["question"] = self.question
        data["context"] = self.context
        data["explanation"] = self.explanation
        
        if self.rating is not None:
            data["rating"] = self.rating

        data["question_id"] = self.question_id
        data["relevant_parts"] = [RelevantPart.to_json(item) for item in self.relevant_parts]
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class RateAnswerRequest:
    rating: Literal["down", "neutral", "up"]
    answer_id: int

    @classmethod
    def from_json(cls, data: dict) -> "RateAnswerRequest":
        return cls(
            rating = data["rating"],
            answer_id = data["answer_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["rating"] = self.rating
        data["answer_id"] = self.answer_id

        return data

@dataclass
class RateAnswerResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "RateAnswerResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class AddItemRequest:
    filename: str
    filetype: Literal["pdf", "html", "xml", "txt", "docx", "md"]
    database_name: str
    folder_name: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "AddItemRequest":
        return cls(
            filename = data["filename"],
            filetype = data["filetype"],
            database_name = data["database_name"],
            folder_name = data["folder_name"] if "folder_name" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        data["filename"] = self.filename
        data["filetype"] = self.filetype
        data["database_name"] = self.database_name
        
        if self.folder_name is not None:
            data["folder_name"] = self.folder_name


        return data

@dataclass
class AddItemResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "AddItemResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class ScrapeRequest:
    urls: list[str]
    database_name: str
    depths: Optional[list[int]]
    external: Optional[bool]
    dynamic: Optional[bool]
    folder_name: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "ScrapeRequest":
        return cls(
            urls = data["urls"],
            database_name = data["database_name"],
            depths = data["depths"] if "depths" in data else None,
            external = data["external"] if "external" in data else None,
            dynamic = data["dynamic"] if "dynamic" in data else None,
            folder_name = data["folder_name"] if "folder_name" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        data["urls"] = self.urls
        data["database_name"] = self.database_name
        
        if self.depths is not None:
            data["depths"] = self.depths

        
        if self.external is not None:
            data["external"] = self.external

        
        if self.dynamic is not None:
            data["dynamic"] = self.dynamic

        
        if self.folder_name is not None:
            data["folder_name"] = self.folder_name


        return data

@dataclass
class ScrapeResponse:
    succes: bool
    message: str
    done: bool
    nitems: int
    nerror: int
    nskip: int
    nlink: int

    @classmethod
    def from_json(cls, data: dict) -> "ScrapeResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            nitems = data["nitems"],
            nerror = data["nerror"],
            nskip = data["nskip"],
            nlink = data["nlink"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["nitems"] = self.nitems
        data["nerror"] = self.nerror
        data["nskip"] = self.nskip
        data["nlink"] = self.nlink

        return data

@dataclass
class ScrapeUpdateResponse:
    task: str
    total: Optional[int]
    count: Optional[int]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "ScrapeUpdateResponse":
        return cls(
            task = data["task"],
            total = data["total"] if "total" in data else None,
            count = data["count"] if "count" in data else None,
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["task"] = self.task
        
        if self.total is not None:
            data["total"] = self.total

        
        if self.count is not None:
            data["count"] = self.count

        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class ItemInfoRequest:
    item_id: int

    @classmethod
    def from_json(cls, data: dict) -> "ItemInfoRequest":
        return cls(
            item_id = data["item_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["item_id"] = self.item_id

        return data

@dataclass
class ItemLink:
    name: str
    id: int

    @classmethod
    def from_json(cls, data: dict) -> "ItemLink":
        return cls(
            name = data["name"],
            id = data["id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["name"] = self.name
        data["id"] = self.id

        return data

@dataclass
class ItemInfoResponse:
    id: int
    name: str
    type: str
    folder: Optional[str]
    url: Optional[str]
    outgoing_links: list[ItemLink]
    incoming_links: list[ItemLink]
    storage_name: Optional[str]
    created_at: DateTime
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "ItemInfoResponse":
        return cls(
            id = data["id"],
            name = data["name"],
            type = data["type"],
            folder = data["folder"] if "folder" in data else None,
            url = data["url"] if "url" in data else None,
            outgoing_links = [ItemLink.from_json(item) for item in data["outgoing_links"]],
            incoming_links = [ItemLink.from_json(item) for item in data["incoming_links"]],
            storage_name = data["storage_name"] if "storage_name" in data else None,
            created_at = DateTime.from_json(data['created_at']),
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["type"] = self.type
        
        if self.folder is not None:
            data["folder"] = self.folder

        
        if self.url is not None:
            data["url"] = self.url

        data["outgoing_links"] = [ItemLink.to_json(item) for item in self.outgoing_links]
        data["incoming_links"] = [ItemLink.to_json(item) for item in self.incoming_links]
        
        if self.storage_name is not None:
            data["storage_name"] = self.storage_name

        data["created_at"] = self.created_at.to_json()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteItemRequest:
    item_id: int

    @classmethod
    def from_json(cls, data: dict) -> "DeleteItemRequest":
        return cls(
            item_id = data["item_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["item_id"] = self.item_id

        return data

@dataclass
class DeleteItemResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteItemResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class RenameItemRequest:
    item_id: int
    new_name: str

    @classmethod
    def from_json(cls, data: dict) -> "RenameItemRequest":
        return cls(
            item_id = data["item_id"],
            new_name = data["new_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["item_id"] = self.item_id
        data["new_name"] = self.new_name

        return data

@dataclass
class RenameItemResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "RenameItemResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class MoveItemRequest:
    item_id: int
    new_folder: str

    @classmethod
    def from_json(cls, data: dict) -> "MoveItemRequest":
        return cls(
            item_id = data["item_id"],
            new_folder = data["new_folder"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["item_id"] = self.item_id
        data["new_folder"] = self.new_folder

        return data

@dataclass
class MoveItemResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "MoveItemResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteFolderRequest:
    folder_name: str
    database_name: str

    @classmethod
    def from_json(cls, data: dict) -> "DeleteFolderRequest":
        return cls(
            folder_name = data["folder_name"],
            database_name = data["database_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["folder_name"] = self.folder_name
        data["database_name"] = self.database_name

        return data

@dataclass
class DeleteFolderResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteFolderResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class BuildRequest:
    database_name: str
    build_name: str

    @classmethod
    def from_json(cls, data: dict) -> "BuildRequest":
        return cls(
            database_name = data["database_name"],
            build_name = data["build_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name
        data["build_name"] = self.build_name

        return data

@dataclass
class BuildResponse:
    succes: bool
    message: str
    done: bool
    nitems: int
    nerror: int

    @classmethod
    def from_json(cls, data: dict) -> "BuildResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            nitems = data["nitems"],
            nerror = data["nerror"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["nitems"] = self.nitems
        data["nerror"] = self.nerror

        return data

@dataclass
class BuildUpdateResponse:
    task: str
    total: Optional[int]
    count: Optional[int]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "BuildUpdateResponse":
        return cls(
            task = data["task"],
            total = data["total"] if "total" in data else None,
            count = data["count"] if "count" in data else None,
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["task"] = self.task
        
        if self.total is not None:
            data["total"] = self.total

        
        if self.count is not None:
            data["count"] = self.count

        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class UpdateBuildRequest:
    database_name: str
    build_name: str

    @classmethod
    def from_json(cls, data: dict) -> "UpdateBuildRequest":
        return cls(
            database_name = data["database_name"],
            build_name = data["build_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["database_name"] = self.database_name
        data["build_name"] = self.build_name

        return data

@dataclass
class UpdateBuildResponse:
    succes: bool
    message: str
    done: bool
    nitems: int
    nerror: int

    @classmethod
    def from_json(cls, data: dict) -> "UpdateBuildResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
            nitems = data["nitems"],
            nerror = data["nerror"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done
        data["nitems"] = self.nitems
        data["nerror"] = self.nerror

        return data

@dataclass
class UpdateBuildUpdateResponse:
    task: str
    total: Optional[int]
    count: Optional[int]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "UpdateBuildUpdateResponse":
        return cls(
            task = data["task"],
            total = data["total"] if "total" in data else None,
            count = data["count"] if "count" in data else None,
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["task"] = self.task
        
        if self.total is not None:
            data["total"] = self.total

        
        if self.count is not None:
            data["count"] = self.count

        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class RenameBuildRequest:
    build_id: int
    new_name: str

    @classmethod
    def from_json(cls, data: dict) -> "RenameBuildRequest":
        return cls(
            build_id = data["build_id"],
            new_name = data["new_name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["build_id"] = self.build_id
        data["new_name"] = self.new_name

        return data

@dataclass
class RenameBuildResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "RenameBuildResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteBuildRequest:
    build_id: int

    @classmethod
    def from_json(cls, data: dict) -> "DeleteBuildRequest":
        return cls(
            build_id = data["build_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["build_id"] = self.build_id

        return data

@dataclass
class DeleteBuildResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteBuildResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class BuildInfoRequest:
    build_id: int

    @classmethod
    def from_json(cls, data: dict) -> "BuildInfoRequest":
        return cls(
            build_id = data["build_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["build_id"] = self.build_id

        return data

@dataclass
class BuildInfoQuestion:
    id: int
    first_message: str
    created_at: DateTime

    @classmethod
    def from_json(cls, data: dict) -> "BuildInfoQuestion":
        return cls(
            id = data["id"],
            first_message = data["first_message"],
            created_at = DateTime.from_json(data['created_at']),
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["first_message"] = self.first_message
        data["created_at"] = self.created_at.to_json()

        return data

@dataclass
class BuildInfoItem:
    id: int
    name: str

    @classmethod
    def from_json(cls, data: dict) -> "BuildInfoItem":
        return cls(
            id = data["id"],
            name = data["name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name

        return data

@dataclass
class BuildInfoResponse:
    id: int
    name: str
    created_at: DateTime
    database_id: int
    question: list[BuildInfoQuestion]
    items: list[BuildInfoItem]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "BuildInfoResponse":
        return cls(
            id = data["id"],
            name = data["name"],
            created_at = DateTime.from_json(data['created_at']),
            database_id = data["database_id"],
            question = [BuildInfoQuestion.from_json(item) for item in data["question"]],
            items = [BuildInfoItem.from_json(item) for item in data["items"]],
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["created_at"] = self.created_at.to_json()
        data["database_id"] = self.database_id
        data["question"] = [BuildInfoQuestion.to_json(item) for item in self.question]
        data["items"] = [BuildInfoItem.to_json(item) for item in self.items]
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class CreateUserRequest:
    password: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "CreateUserRequest":
        return cls(
            password = data["password"],
            email = data["email"],
            first_name = data["first_name"] if "first_name" in data else None,
            last_name = data["last_name"] if "last_name" in data else None,
            company = data["company"] if "company" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        data["password"] = self.password
        data["email"] = self.email
        
        if self.first_name is not None:
            data["first_name"] = self.first_name

        
        if self.last_name is not None:
            data["last_name"] = self.last_name

        
        if self.company is not None:
            data["company"] = self.company


        return data

@dataclass
class CreateUserResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "CreateUserResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class LoginRequest:
    email: str
    password: str

    @classmethod
    def from_json(cls, data: dict) -> "LoginRequest":
        return cls(
            email = data["email"],
            password = data["password"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["email"] = self.email
        data["password"] = self.password

        return data

@dataclass
class LoginResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "LoginResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class LogoutResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "LogoutResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class OAuthRequest:
    provider: Literal["twitter", "google", "github", "facebook"]

    @classmethod
    def from_json(cls, data: dict) -> "OAuthRequest":
        return cls(
            provider = data["provider"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["provider"] = self.provider

        return data

@dataclass
class OAuthResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "OAuthResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class OAuthAuthorizeRequest:
    provider: Literal["twitter", "google", "github", "facebook"]

    @classmethod
    def from_json(cls, data: dict) -> "OAuthAuthorizeRequest":
        return cls(
            provider = data["provider"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["provider"] = self.provider

        return data

@dataclass
class OAuthAuthorizeResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "OAuthAuthorizeResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class BirthDay:
    day: int
    month: int
    year: int

    @classmethod
    def from_json(cls, data: dict) -> "BirthDay":
        return cls(
            day = data["day"],
            month = data["month"],
            year = data["year"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["day"] = self.day
        data["month"] = self.month
        data["year"] = self.year

        return data

@dataclass
class UpdateProfileRequest:
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    birthday: Optional[BirthDay]

    @classmethod
    def from_json(cls, data: dict) -> "UpdateProfileRequest":
        return cls(
            first_name = data["first_name"] if "first_name" in data else None,
            last_name = data["last_name"] if "last_name" in data else None,
            company = data["company"] if "company" in data else None,
            birthday = data["birthday"] if "birthday" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        
        if self.first_name is not None:
            data["first_name"] = self.first_name

        
        if self.last_name is not None:
            data["last_name"] = self.last_name

        
        if self.company is not None:
            data["company"] = self.company

        
        if self.birthday is not None:
            data["birthday"] = self.birthday


        return data

@dataclass
class UpdateProfileResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "UpdateProfileResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class UserProfile:
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[BirthDay]
    company: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "UserProfile":
        return cls(
            first_name = data["first_name"] if "first_name" in data else None,
            last_name = data["last_name"] if "last_name" in data else None,
            birthday = data["birthday"] if "birthday" in data else None,
            company = data["company"] if "company" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        
        if self.first_name is not None:
            data["first_name"] = self.first_name

        
        if self.last_name is not None:
            data["last_name"] = self.last_name

        
        if self.birthday is not None:
            data["birthday"] = self.birthday

        
        if self.company is not None:
            data["company"] = self.company


        return data

@dataclass
class UserDatabase:
    id: int
    name: str
    permission: Literal["read", "write", "delete", "admin"]

    @classmethod
    def from_json(cls, data: dict) -> "UserDatabase":
        return cls(
            id = data["id"],
            name = data["name"],
            permission = data["permission"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["permission"] = self.permission

        return data

@dataclass
class UserApiToken:
    id: int
    token: str
    name: str
    created_at: DateTime
    last_used_at: Optional[DateTime]

    @classmethod
    def from_json(cls, data: dict) -> "UserApiToken":
        return cls(
            id = data["id"],
            token = data["token"],
            name = data["name"],
            created_at = DateTime.from_json(data['created_at']),
            last_used_at = data["last_used_at"] if "last_used_at" in data else None,
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["token"] = self.token
        data["name"] = self.name
        data["created_at"] = self.created_at.to_json()
        
        if self.last_used_at is not None:
            data["last_used_at"] = self.last_used_at


        return data

@dataclass
class UserInfoResponse:
    id: int
    email: str
    created_at: DateTime
    profile: UserProfile
    databases: list[UserDatabase]
    tokens: list[UserApiToken]
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "UserInfoResponse":
        return cls(
            id = data["id"],
            email = data["email"],
            created_at = DateTime.from_json(data['created_at']),
            profile = UserProfile.from_json(data['profile']),
            databases = [UserDatabase.from_json(item) for item in data["databases"]],
            tokens = [UserApiToken.from_json(item) for item in data["tokens"]],
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["id"] = self.id
        data["email"] = self.email
        data["created_at"] = self.created_at.to_json()
        data["profile"] = self.profile.to_json()
        data["databases"] = [UserDatabase.to_json(item) for item in self.databases]
        data["tokens"] = [UserApiToken.to_json(item) for item in self.tokens]
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class UpdatePasswordRequest:
    new_password: str

    @classmethod
    def from_json(cls, data: dict) -> "UpdatePasswordRequest":
        return cls(
            new_password = data["new_password"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["new_password"] = self.new_password

        return data

@dataclass
class UpdatePasswordResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "UpdatePasswordResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class UpdateEmailRequest:
    new_email: str

    @classmethod
    def from_json(cls, data: dict) -> "UpdateEmailRequest":
        return cls(
            new_email = data["new_email"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["new_email"] = self.new_email

        return data

@dataclass
class UpdateEmailResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "UpdateEmailResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteUserResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteUserResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class CreateTokenRequest:
    name: str

    @classmethod
    def from_json(cls, data: dict) -> "CreateTokenRequest":
        return cls(
            name = data["name"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["name"] = self.name

        return data

@dataclass
class CreateTokenResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "CreateTokenResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data

@dataclass
class DeleteTokenRequest:
    token_id: int

    @classmethod
    def from_json(cls, data: dict) -> "DeleteTokenRequest":
        return cls(
            token_id = data["token_id"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["token_id"] = self.token_id

        return data

@dataclass
class DeleteTokenResponse:
    succes: bool
    message: str
    done: bool

    @classmethod
    def from_json(cls, data: dict) -> "DeleteTokenResponse":
        return cls(
            succes = data["succes"],
            message = data["message"],
            done = data["done"],
        )

    def to_json(self) -> dict:
        data = dict()
        data["succes"] = self.succes
        data["message"] = self.message
        data["done"] = self.done

        return data
import requests
import aiohttp

import os
import json
from typing import Optional, Generator, AsyncGenerator, Union


class KayocApi:

    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
        asession: Optional[aiohttp.ClientSession] = None,
        base_url: Optional[str] = None,
    ):
        self.session = requests.Session() if session is None else session
        self.asession = aiohttp.ClientSession() if asession is None else asession
        self.base_url = "https://api.kayoc.nl" if base_url is None else base_url
        self.api_key = os.environ.get("KAYOC_API_KEY") if api_key is None else api_key

        if self.api_key is not None:
            self.session.headers.update({"Authorization": "Bearer " + self.api_key})

    def __repr__(self):
        return "{}({})".format(KayocApi, self.base_url)

    def __str__(self):
        return "{}({})".format(KayocApi, self.base_url)

    async def close(self):
        self.session.close()
        await self.asession.close()

    def database_create(
        self, database_name: str
    ) -> Union[CreateDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/create"
            data = CreateDatabaseRequest(database_name=database_name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return CreateDatabaseResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_create_async(
        self, database_name: str
    ) -> Union[CreateDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/create"
            async with self.asession.post(
                url, json=CreateDatabaseRequest(database_name=database_name).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return CreateDatabaseResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_delete(
        self, database_name: str
    ) -> Union[DeleteDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/delete"
            data = DeleteDatabaseRequest(database_name=database_name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteDatabaseResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_delete_async(
        self, database_name: str
    ) -> Union[DeleteDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/delete"
            async with self.asession.post(
                url, json=DeleteDatabaseRequest(database_name=database_name).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteDatabaseResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_info(
        self, database_name: str
    ) -> Union[DatabaseInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/info"
            data = DatabaseInfoRequest(database_name=database_name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DatabaseInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_info_async(
        self, database_name: str
    ) -> Union[DatabaseInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/info"
            async with self.asession.post(
                url, json=DatabaseInfoRequest(database_name=database_name).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DatabaseInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_rename(
        self, database_name: str, new_name: str
    ) -> Union[RenameDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/rename"
            data = RenameDatabaseRequest(
                database_name=database_name, new_name=new_name
            ).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return RenameDatabaseResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_rename_async(
        self, database_name: str, new_name: str
    ) -> Union[RenameDatabaseResponse, KayocError]:
        try:
            url = self.base_url + "/database/rename"
            async with self.asession.post(
                url,
                json=RenameDatabaseRequest(
                    database_name=database_name, new_name=new_name
                ).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return RenameDatabaseResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_question_info(
        self, question_id: int
    ) -> Union[QuestionInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/question/info"
            data = QuestionInfoRequest(question_id=question_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return QuestionInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_question_info_async(
        self, question_id: int
    ) -> Union[QuestionInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/question/info"
            async with self.asession.post(
                url, json=QuestionInfoRequest(question_id=question_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return QuestionInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_answer_create(
        self,
        question: str,
        database_name: str,
        keywords: Optional[list[str]] = None,
        question_id: Optional[int] = None,
        build_name: Optional[str] = None,
    ) -> Generator[
        Union[CreateAnswerResponse, KayocError, CreateAnswerUpdateResponse], None, None
    ]:
        url = self.base_url + "/database/answer/create"

        try:
            response = self.session.post(
                url,
                json=CreateAnswerRequest(
                    question=question,
                    database_name=database_name,
                    keywords=keywords,
                    question_id=question_id,
                    build_name=build_name,
                ).to_json(),
                stream=True,
            )

            if response.status_code == 401:
                yield KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )
                return

            if not response.ok:
                yield KayocError.from_json(response.json())
                return

            for update in response.iter_lines():
                update = json.loads(update)
                if update["done"]:
                    if not update["succes"]:
                        yield KayocError.from_json(update)
                    else:
                        yield CreateAnswerResponse.from_json(update)
                    return
                else:
                    yield CreateAnswerUpdateResponse.from_json(update)
        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

        yield KayocError(
            message="Server did not return a done message",
            succes=False,
            error="",
            done=True,
        )

    async def database_answer_create_async(
        self,
        question: str,
        database_name: str,
        keywords: Optional[list[str]] = None,
        question_id: Optional[int] = None,
        build_name: Optional[str] = None,
    ) -> AsyncGenerator[
        Union[CreateAnswerResponse, KayocError, CreateAnswerUpdateResponse], None
    ]:
        url = self.base_url + "/database/answer/create"
        try:
            async with self.asession.post(
                url,
                json=CreateAnswerRequest(
                    question=question,
                    database_name=database_name,
                    keywords=keywords,
                    question_id=question_id,
                    build_name=build_name,
                ).to_json(),
                headers={"Content-Type": "application/json"},
                stream=True,
            ) as response:

                if response.status == 401:
                    yield KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )
                    return

                if response.status // 100 != 2:
                    yield KayocError.from_json(await response.json())
                    return

                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    while b"\\n" in buffer:
                        line, buffer = buffer.split(b"\\n", 1)
                        update = json.loads(line)
                        if update["done"]:
                            if not update["succes"]:
                                yield KayocError.from_json(update)
                            else:
                                yield CreateAnswerResponse.from_json(update)
                            return
                        else:
                            yield CreateAnswerUpdateResponse.from_json(update)
                yield KayocError(
                    message="Server did not return a done message",
                    succes=False,
                    error="sdnrdm",
                    done=True,
                )

        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_answer_info(
        self, answer_id: int
    ) -> Union[AnswerInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/answer/info"
            data = AnswerInfoRequest(answer_id=answer_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return AnswerInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_answer_info_async(
        self, answer_id: int
    ) -> Union[AnswerInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/answer/info"
            async with self.asession.post(
                url, json=AnswerInfoRequest(answer_id=answer_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return AnswerInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_answer_rate(
        self, rating: Literal["down", "neutral", "up"], answer_id: int
    ) -> Union[RateAnswerResponse, KayocError]:
        try:
            url = self.base_url + "/database/answer/rate"
            data = RateAnswerRequest(rating=rating, answer_id=answer_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return RateAnswerResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_answer_rate_async(
        self, rating: Literal["down", "neutral", "up"], answer_id: int
    ) -> Union[RateAnswerResponse, KayocError]:
        try:
            url = self.base_url + "/database/answer/rate"
            async with self.asession.post(
                url,
                json=RateAnswerRequest(rating=rating, answer_id=answer_id).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return RateAnswerResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_add(
        self,
        filename: str,
        filetype: Literal["pdf", "html", "xml", "txt", "docx", "md"],
        database_name: str,
        folder_name: Optional[str] = None,
    ) -> Union[AddItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/add"
            data = AddItemRequest(
                filename=filename,
                filetype=filetype,
                database_name=database_name,
                folder_name=folder_name,
            ).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return AddItemResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_add_async(
        self,
        filename: str,
        filetype: Literal["pdf", "html", "xml", "txt", "docx", "md"],
        database_name: str,
        folder_name: Optional[str] = None,
    ) -> Union[AddItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/add"
            async with self.asession.post(
                url,
                json=AddItemRequest(
                    filename=filename,
                    filetype=filetype,
                    database_name=database_name,
                    folder_name=folder_name,
                ).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return AddItemResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_scrape(
        self,
        urls: list[str],
        database_name: str,
        depths: Optional[list[int]] = None,
        external: Optional[bool] = None,
        dynamic: Optional[bool] = None,
        folder_name: Optional[str] = None,
    ) -> Generator[Union[ScrapeResponse, KayocError, ScrapeUpdateResponse], None, None]:
        url = self.base_url + "/database/item/scrape"

        try:
            response = self.session.post(
                url,
                json=ScrapeRequest(
                    urls=urls,
                    database_name=database_name,
                    depths=depths,
                    external=external,
                    dynamic=dynamic,
                    folder_name=folder_name,
                ).to_json(),
                stream=True,
            )

            if response.status_code == 401:
                yield KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )
                return

            if not response.ok:
                yield KayocError.from_json(response.json())
                return

            for update in response.iter_lines():
                update = json.loads(update)
                if update["done"]:
                    if not update["succes"]:
                        yield KayocError.from_json(update)
                    else:
                        yield ScrapeResponse.from_json(update)
                    return
                else:
                    yield ScrapeUpdateResponse.from_json(update)
        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

        yield KayocError(
            message="Server did not return a done message",
            succes=False,
            error="",
            done=True,
        )

    async def database_item_scrape_async(
        self,
        urls: list[str],
        database_name: str,
        depths: Optional[list[int]] = None,
        external: Optional[bool] = None,
        dynamic: Optional[bool] = None,
        folder_name: Optional[str] = None,
    ) -> AsyncGenerator[Union[ScrapeResponse, KayocError, ScrapeUpdateResponse], None]:
        url = self.base_url + "/database/item/scrape"
        try:
            async with self.asession.post(
                url,
                json=ScrapeRequest(
                    urls=urls,
                    database_name=database_name,
                    depths=depths,
                    external=external,
                    dynamic=dynamic,
                    folder_name=folder_name,
                ).to_json(),
                headers={"Content-Type": "application/json"},
                stream=True,
            ) as response:

                if response.status == 401:
                    yield KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )
                    return

                if response.status // 100 != 2:
                    yield KayocError.from_json(await response.json())
                    return

                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    while b"\\n" in buffer:
                        line, buffer = buffer.split(b"\\n", 1)
                        update = json.loads(line)
                        if update["done"]:
                            if not update["succes"]:
                                yield KayocError.from_json(update)
                            else:
                                yield ScrapeResponse.from_json(update)
                            return
                        else:
                            yield ScrapeUpdateResponse.from_json(update)
                yield KayocError(
                    message="Server did not return a done message",
                    succes=False,
                    error="sdnrdm",
                    done=True,
                )

        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_info(self, item_id: int) -> Union[ItemInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/info"
            data = ItemInfoRequest(item_id=item_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return ItemInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_info_async(
        self, item_id: int
    ) -> Union[ItemInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/info"
            async with self.asession.post(
                url, json=ItemInfoRequest(item_id=item_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return ItemInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_delete(
        self, item_id: int
    ) -> Union[DeleteItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/delete"
            data = DeleteItemRequest(item_id=item_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteItemResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_delete_async(
        self, item_id: int
    ) -> Union[DeleteItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/delete"
            async with self.asession.post(
                url, json=DeleteItemRequest(item_id=item_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteItemResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_rename(
        self, item_id: int, new_name: str
    ) -> Union[RenameItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/rename"
            data = RenameItemRequest(item_id=item_id, new_name=new_name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return RenameItemResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_rename_async(
        self, item_id: int, new_name: str
    ) -> Union[RenameItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/rename"
            async with self.asession.post(
                url,
                json=RenameItemRequest(item_id=item_id, new_name=new_name).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return RenameItemResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_move(
        self, item_id: int, new_folder: str
    ) -> Union[MoveItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/move"
            data = MoveItemRequest(item_id=item_id, new_folder=new_folder).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return MoveItemResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_move_async(
        self, item_id: int, new_folder: str
    ) -> Union[MoveItemResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/move"
            async with self.asession.post(
                url,
                json=MoveItemRequest(item_id=item_id, new_folder=new_folder).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return MoveItemResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_item_folder_delete(
        self, folder_name: str, database_name: str
    ) -> Union[DeleteFolderResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/folder/delete"
            data = DeleteFolderRequest(
                folder_name=folder_name, database_name=database_name
            ).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteFolderResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_item_folder_delete_async(
        self, folder_name: str, database_name: str
    ) -> Union[DeleteFolderResponse, KayocError]:
        try:
            url = self.base_url + "/database/item/folder/delete"
            async with self.asession.post(
                url,
                json=DeleteFolderRequest(
                    folder_name=folder_name, database_name=database_name
                ).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteFolderResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_build_create(
        self, database_name: str, build_name: str
    ) -> Generator[Union[BuildResponse, KayocError, BuildUpdateResponse], None, None]:
        url = self.base_url + "/database/build/create"

        try:
            response = self.session.post(
                url,
                json=BuildRequest(
                    database_name=database_name, build_name=build_name
                ).to_json(),
                stream=True,
            )

            if response.status_code == 401:
                yield KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )
                return

            if not response.ok:
                yield KayocError.from_json(response.json())
                return

            for update in response.iter_lines():
                update = json.loads(update)
                if update["done"]:
                    if not update["succes"]:
                        yield KayocError.from_json(update)
                    else:
                        yield BuildResponse.from_json(update)
                    return
                else:
                    yield BuildUpdateResponse.from_json(update)
        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

        yield KayocError(
            message="Server did not return a done message",
            succes=False,
            error="",
            done=True,
        )

    async def database_build_create_async(
        self, database_name: str, build_name: str
    ) -> AsyncGenerator[Union[BuildResponse, KayocError, BuildUpdateResponse], None]:
        url = self.base_url + "/database/build/create"
        try:
            async with self.asession.post(
                url,
                json=BuildRequest(
                    database_name=database_name, build_name=build_name
                ).to_json(),
                headers={"Content-Type": "application/json"},
                stream=True,
            ) as response:

                if response.status == 401:
                    yield KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )
                    return

                if response.status // 100 != 2:
                    yield KayocError.from_json(await response.json())
                    return

                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    while b"\\n" in buffer:
                        line, buffer = buffer.split(b"\\n", 1)
                        update = json.loads(line)
                        if update["done"]:
                            if not update["succes"]:
                                yield KayocError.from_json(update)
                            else:
                                yield BuildResponse.from_json(update)
                            return
                        else:
                            yield BuildUpdateResponse.from_json(update)
                yield KayocError(
                    message="Server did not return a done message",
                    succes=False,
                    error="sdnrdm",
                    done=True,
                )

        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_build_update(
        self, database_name: str, build_name: str
    ) -> Generator[
        Union[UpdateBuildResponse, KayocError, UpdateBuildUpdateResponse], None, None
    ]:
        url = self.base_url + "/database/build/update"

        try:
            response = self.session.post(
                url,
                json=UpdateBuildRequest(
                    database_name=database_name, build_name=build_name
                ).to_json(),
                stream=True,
            )

            if response.status_code == 401:
                yield KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )
                return

            if not response.ok:
                yield KayocError.from_json(response.json())
                return

            for update in response.iter_lines():
                update = json.loads(update)
                if update["done"]:
                    if not update["succes"]:
                        yield KayocError.from_json(update)
                    else:
                        yield UpdateBuildResponse.from_json(update)
                    return
                else:
                    yield UpdateBuildUpdateResponse.from_json(update)
        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

        yield KayocError(
            message="Server did not return a done message",
            succes=False,
            error="",
            done=True,
        )

    async def database_build_update_async(
        self, database_name: str, build_name: str
    ) -> AsyncGenerator[
        Union[UpdateBuildResponse, KayocError, UpdateBuildUpdateResponse], None
    ]:
        url = self.base_url + "/database/build/update"
        try:
            async with self.asession.post(
                url,
                json=UpdateBuildRequest(
                    database_name=database_name, build_name=build_name
                ).to_json(),
                headers={"Content-Type": "application/json"},
                stream=True,
            ) as response:

                if response.status == 401:
                    yield KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )
                    return

                if response.status // 100 != 2:
                    yield KayocError.from_json(await response.json())
                    return

                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    while b"\\n" in buffer:
                        line, buffer = buffer.split(b"\\n", 1)
                        update = json.loads(line)
                        if update["done"]:
                            if not update["succes"]:
                                yield KayocError.from_json(update)
                            else:
                                yield UpdateBuildResponse.from_json(update)
                            return
                        else:
                            yield UpdateBuildUpdateResponse.from_json(update)
                yield KayocError(
                    message="Server did not return a done message",
                    succes=False,
                    error="sdnrdm",
                    done=True,
                )

        except Exception as e:
            yield KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_build_rename(
        self, build_id: int, new_name: str
    ) -> Union[RenameBuildResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/rename"
            data = RenameBuildRequest(build_id=build_id, new_name=new_name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return RenameBuildResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_build_rename_async(
        self, build_id: int, new_name: str
    ) -> Union[RenameBuildResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/rename"
            async with self.asession.post(
                url,
                json=RenameBuildRequest(build_id=build_id, new_name=new_name).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return RenameBuildResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_build_delete(
        self, build_id: int
    ) -> Union[DeleteBuildResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/delete"
            data = DeleteBuildRequest(build_id=build_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteBuildResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_build_delete_async(
        self, build_id: int
    ) -> Union[DeleteBuildResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/delete"
            async with self.asession.post(
                url, json=DeleteBuildRequest(build_id=build_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteBuildResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def database_build_info(
        self, build_id: int
    ) -> Union[BuildInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/info"
            data = BuildInfoRequest(build_id=build_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return BuildInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def database_build_info_async(
        self, build_id: int
    ) -> Union[BuildInfoResponse, KayocError]:
        try:
            url = self.base_url + "/database/build/info"
            async with self.asession.post(
                url, json=BuildInfoRequest(build_id=build_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return BuildInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_create(
        self,
        password: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Union[CreateUserResponse, KayocError]:
        try:
            url = self.base_url + "/user/create"
            data = CreateUserRequest(
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                company=company,
            ).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return CreateUserResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_create_async(
        self,
        password: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Union[CreateUserResponse, KayocError]:
        try:
            url = self.base_url + "/user/create"
            async with self.asession.post(
                url,
                json=CreateUserRequest(
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    company=company,
                ).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return CreateUserResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_login(self, email: str, password: str) -> Union[LoginResponse, KayocError]:
        try:
            url = self.base_url + "/user/login"
            data = LoginRequest(email=email, password=password).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return LoginResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_login_async(
        self, email: str, password: str
    ) -> Union[LoginResponse, KayocError]:
        try:
            url = self.base_url + "/user/login"
            async with self.asession.post(
                url, json=LoginRequest(email=email, password=password).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return LoginResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_logout(
        self,
    ) -> Union[LogoutResponse, KayocError]:
        try:
            url = self.base_url + "/user/logout"
            data = None
            response = self.session.get(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return LogoutResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_logout_async(
        self,
    ) -> Union[LogoutResponse, KayocError]:
        try:
            url = self.base_url + "/user/logout"
            async with self.asession.get(url, json=None) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return LogoutResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_oauth_login(
        self, provider: Literal["twitter", "google", "github", "facebook"]
    ) -> Union[OAuthResponse, KayocError]:
        try:
            url = self.base_url + "/user/oauth/login"
            data = OAuthRequest(provider=provider).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return OAuthResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_oauth_login_async(
        self, provider: Literal["twitter", "google", "github", "facebook"]
    ) -> Union[OAuthResponse, KayocError]:
        try:
            url = self.base_url + "/user/oauth/login"
            async with self.asession.post(
                url, json=OAuthRequest(provider=provider).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return OAuthResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_oauth_authorize(
        self, provider: Literal["twitter", "google", "github", "facebook"]
    ) -> Union[OAuthAuthorizeResponse, KayocError]:
        try:
            url = self.base_url + "/user/oauth/authorize"
            data = OAuthAuthorizeRequest(provider=provider).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return OAuthAuthorizeResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_oauth_authorize_async(
        self, provider: Literal["twitter", "google", "github", "facebook"]
    ) -> Union[OAuthAuthorizeResponse, KayocError]:
        try:
            url = self.base_url + "/user/oauth/authorize"
            async with self.asession.post(
                url, json=OAuthAuthorizeRequest(provider=provider).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return OAuthAuthorizeResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_profile_update(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        birthday: Optional[BirthDay] = None,
    ) -> Union[UpdateProfileResponse, KayocError]:
        try:
            url = self.base_url + "/user/profile/update"
            data = UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
                company=company,
                birthday=birthday,
            ).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return UpdateProfileResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_profile_update_async(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        birthday: Optional[BirthDay] = None,
    ) -> Union[UpdateProfileResponse, KayocError]:
        try:
            url = self.base_url + "/user/profile/update"
            async with self.asession.post(
                url,
                json=UpdateProfileRequest(
                    first_name=first_name,
                    last_name=last_name,
                    company=company,
                    birthday=birthday,
                ).to_json(),
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return UpdateProfileResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_info(
        self,
    ) -> Union[UserInfoResponse, KayocError]:
        try:
            url = self.base_url + "/user/info"
            data = None
            response = self.session.get(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return UserInfoResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_info_async(
        self,
    ) -> Union[UserInfoResponse, KayocError]:
        try:
            url = self.base_url + "/user/info"
            async with self.asession.get(url, json=None) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return UserInfoResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_password_update(
        self, new_password: str
    ) -> Union[UpdatePasswordResponse, KayocError]:
        try:
            url = self.base_url + "/user/password/update"
            data = UpdatePasswordRequest(new_password=new_password).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return UpdatePasswordResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_password_update_async(
        self, new_password: str
    ) -> Union[UpdatePasswordResponse, KayocError]:
        try:
            url = self.base_url + "/user/password/update"
            async with self.asession.post(
                url, json=UpdatePasswordRequest(new_password=new_password).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return UpdatePasswordResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_email_update(
        self, new_email: str
    ) -> Union[UpdateEmailResponse, KayocError]:
        try:
            url = self.base_url + "/user/email/update"
            data = UpdateEmailRequest(new_email=new_email).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return UpdateEmailResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_email_update_async(
        self, new_email: str
    ) -> Union[UpdateEmailResponse, KayocError]:
        try:
            url = self.base_url + "/user/email/update"
            async with self.asession.post(
                url, json=UpdateEmailRequest(new_email=new_email).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return UpdateEmailResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_delete(
        self,
    ) -> Union[DeleteUserResponse, KayocError]:
        try:
            url = self.base_url + "/user/delete"
            data = None
            response = self.session.get(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteUserResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_delete_async(
        self,
    ) -> Union[DeleteUserResponse, KayocError]:
        try:
            url = self.base_url + "/user/delete"
            async with self.asession.get(url, json=None) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteUserResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_token_create(self, name: str) -> Union[CreateTokenResponse, KayocError]:
        try:
            url = self.base_url + "/user/token/create"
            data = CreateTokenRequest(name=name).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return CreateTokenResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_token_create_async(
        self, name: str
    ) -> Union[CreateTokenResponse, KayocError]:
        try:
            url = self.base_url + "/user/token/create"
            async with self.asession.post(
                url, json=CreateTokenRequest(name=name).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return CreateTokenResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    def user_token_delete(
        self, token_id: int
    ) -> Union[DeleteTokenResponse, KayocError]:
        try:
            url = self.base_url + "/user/token/delete"
            data = DeleteTokenRequest(token_id=token_id).to_json()
            response = self.session.post(url, json=data)

            if response.status_code == 401:
                return KayocError(
                    message="You are not logged in",
                    succes=False,
                    error="nli",
                    done=True,
                )

            if response.status_code // 100 != 2:
                return KayocError.from_json(response.json())

            return DeleteTokenResponse.from_json(response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )

    async def user_token_delete_async(
        self, token_id: int
    ) -> Union[DeleteTokenResponse, KayocError]:
        try:
            url = self.base_url + "/user/token/delete"
            async with self.asession.post(
                url, json=DeleteTokenRequest(token_id=token_id).to_json()
            ) as response:

                if response.status == 401:
                    return KayocError(
                        message="You are not logged in",
                        succes=False,
                        error="nli",
                        done=True,
                    )

                if response.status // 100 != 2:
                    return KayocError.from_json(await response.json())

                return DeleteTokenResponse.from_json(await response.json())
        except Exception as e:
            return KayocError(
                message=f"An error was raised in the client: {e}",
                succes=False,
                error="sww",
                done=True,
            )
