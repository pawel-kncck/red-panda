from typing import Any
import uuid

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    User, UserCreate, UserUpdate,
    Conversation, ConversationCreate, ConversationUpdate,
    Message, MessageCreate,
    CodeBlock, CodeBlockCreate, CodeBlockUpdate,
    File, FileCreate
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# ============== Conversation CRUD ==============
def create_conversation(
    *, session: Session, conversation_in: ConversationCreate, user_id: uuid.UUID
) -> Conversation:
    db_obj = Conversation.model_validate(
        conversation_in, update={"user_id": user_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_conversation(
    *, session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID
) -> Conversation | None:
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    return session.exec(statement).first()


def get_conversations(
    *, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[Conversation]:
    statement = select(Conversation).where(
        Conversation.user_id == user_id
    ).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_conversation(
    *, session: Session, db_conversation: Conversation, conversation_in: ConversationUpdate
) -> Conversation:
    conversation_data = conversation_in.model_dump(exclude_unset=True)
    db_conversation.sqlmodel_update(conversation_data)
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation


def delete_conversation(
    *, session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = session.exec(statement).first()
    if conversation:
        session.delete(conversation)
        session.commit()
        return True
    return False


# ============== Message CRUD ==============
def create_message(
    *, session: Session, message_in: MessageCreate, conversation_id: uuid.UUID
) -> Message:
    db_obj = Message.model_validate(
        message_in, update={"conversation_id": conversation_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_messages(
    *, session: Session, conversation_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[Message]:
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).offset(skip).limit(limit)
    return list(session.exec(statement).all())


# ============== CodeBlock CRUD ==============
def create_code_block(
    *, session: Session, code_block_in: CodeBlockCreate, 
    conversation_id: uuid.UUID, user_id: uuid.UUID, message_id: uuid.UUID | None = None
) -> CodeBlock:
    db_obj = CodeBlock.model_validate(
        code_block_in, 
        update={
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message_id": message_id
        }
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_code_block(
    *, session: Session, code_block_id: uuid.UUID, user_id: uuid.UUID
) -> CodeBlock | None:
    statement = select(CodeBlock).where(
        CodeBlock.id == code_block_id,
        CodeBlock.user_id == user_id
    )
    return session.exec(statement).first()


def get_code_blocks(
    *, session: Session, user_id: uuid.UUID, 
    conversation_id: uuid.UUID | None = None,
    skip: int = 0, limit: int = 100
) -> list[CodeBlock]:
    statement = select(CodeBlock).where(CodeBlock.user_id == user_id)
    
    if conversation_id:
        statement = statement.where(CodeBlock.conversation_id == conversation_id)
    
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_code_block(
    *, session: Session, db_code_block: CodeBlock, code_block_in: CodeBlockUpdate
) -> CodeBlock:
    code_block_data = code_block_in.model_dump(exclude_unset=True)
    db_code_block.sqlmodel_update(code_block_data)
    session.add(db_code_block)
    session.commit()
    session.refresh(db_code_block)
    return db_code_block


def delete_code_block(
    *, session: Session, code_block_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    statement = select(CodeBlock).where(
        CodeBlock.id == code_block_id,
        CodeBlock.user_id == user_id
    )
    code_block = session.exec(statement).first()
    if code_block:
        session.delete(code_block)
        session.commit()
        return True
    return False


# ============== File CRUD ==============
def create_file(
    *, session: Session, file_in: FileCreate, user_id: uuid.UUID,
    file_path: str, conversation_id: uuid.UUID | None = None
) -> File:
    db_obj = File.model_validate(
        file_in,
        update={
            "user_id": user_id,
            "file_path": file_path,
            "conversation_id": conversation_id
        }
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_file(
    *, session: Session, file_id: uuid.UUID, user_id: uuid.UUID
) -> File | None:
    statement = select(File).where(
        File.id == file_id,
        File.user_id == user_id
    )
    return session.exec(statement).first()


def get_files(
    *, session: Session, user_id: uuid.UUID,
    conversation_id: uuid.UUID | None = None,
    skip: int = 0, limit: int = 100
) -> list[File]:
    statement = select(File).where(File.user_id == user_id)
    
    if conversation_id:
        statement = statement.where(File.conversation_id == conversation_id)
    
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def delete_file(
    *, session: Session, file_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    statement = select(File).where(
        File.id == file_id,
        File.user_id == user_id
    )
    file = session.exec(statement).first()
    if file:
        session.delete(file)
        session.commit()
        return True
    return False
