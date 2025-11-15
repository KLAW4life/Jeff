from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime

class JournalEntry(EmbeddedDocument):
    date = fields.DateTimeField(default=datetime.utcnow)
    location = fields.StringField()
    title = fields.StringField()
    message = fields.StringField()
    image_url = fields.StringField()
    emotion = fields.StringField()
    ai_response = fields.StringField()

class Patient(Document):
    name = fields.StringField(required=True)
    diagnosis_level = fields.StringField()
    emergency_contact_name = fields.StringField()
    emergency_contact_phone = fields.StringField()
    dob = fields.DateField()
    journal_entries = fields.EmbeddedDocumentListField(JournalEntry)

class User(Document):
    email = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
    role = fields.StringField(choices=["caretaker", "med_professional"])
    # References
    patient = fields.ReferenceField(Patient)

class Image(Document):
    img_name = fields.StringField()
    img_description = fields.StringField()