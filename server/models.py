from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db

class LanguageClassification(db.Model, SerializerMixin):
    
    serialize_rules = ('-languages.classification',)
    
    __tablename__ = 'classifications'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    geographic_location = db.Column(db.String, nullable=False)
    # Relationships
    languages = db.relationship('Language', back_populates='classification', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Language Classification {self.id}, {self.name}, {self.geographic_location}>"
    
class Language(db.Model, SerializerMixin):
    
    serialize_rules = ('-classification.languages',)
    
    __tablename__ = 'languages'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    number_of_speakers = db.Column(db.Integer, db.CheckConstraint('number_of_speakers >= 0', name='check_speakers_constraint'), nullable=False)
    country_of_origin = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('ALIVE', 'ENDANGERED', 'DEAD', 'EXTINCT', name="status_enum"), nullable=False)
    # Foreign Key
    classification_id = db.Column(db.Integer, db.ForeignKey('classifications.id'))
    classification = db.relationship('LanguageClassification', back_populates='languages')
    
    def __repr__(self):
        return f"<Language {self.id}, {self.name}, {self.number_of_speakers}, {self.country_of_origin}, {self.status}, {self.classification_id}"
    
    @validates("status")
    def validate_status(self, key, status):
        status = status.upper()
        if status not in ["ALIVE", "ENDANGERED", "DEAD", "EXTINCT"]:
            raise ValueError(f"{status} is not a valid {key}.")
        return status