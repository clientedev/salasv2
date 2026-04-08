from app import db
from datetime import datetime

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    admin_password = db.Column(db.String(255), nullable=False)
    logo_data = db.Column(db.LargeBinary, nullable=True)
    logo_mimetype = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with classrooms
    classrooms = db.relationship('Classroom', backref='school', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<School {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else ''
        }

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    has_computers = db.Column(db.Boolean, default=False)
    software = db.Column(db.Text, default='')
    description = db.Column(db.Text, default='')
    block = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(255), default='')  # Store filename instead of URL
    excel_filename = db.Column(db.String(255), default='')  # Store Excel filename
    image_data = db.Column(db.LargeBinary)  # Store image data in PostgreSQL (BYTEA)
    excel_data = db.Column(db.LargeBinary)  # Store Excel file data in PostgreSQL (BYTEA)
    image_mimetype = db.Column(db.String(100))  # Store image MIME type
    excel_mimetype = db.Column(db.String(100))  # Store Excel MIME type
    admin_password = db.Column(db.String(255), default='')  # Admin password for classroom access
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True) # Temporarily nullable for migration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name='', capacity=0, has_computers=False, software='', description='', block='', image_filename='', excel_filename='', admin_password='', school_id=None):
        self.name = name
        self.capacity = capacity
        self.has_computers = has_computers
        self.software = software
        self.description = description
        self.block = block
        self.image_filename = image_filename
        self.excel_filename = excel_filename
        self.admin_password = admin_password
        self.school_id = school_id
    
    # Relationship with schedules
    schedules = db.relationship('Schedule', backref='classroom', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Classroom {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'has_computers': self.has_computers,
            'software': self.software,
            'description': self.description,
            'block': self.block,
            'excel_filename': self.excel_filename
        }

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    shift = db.Column(db.String(20), nullable=False)  # morning, afternoon, fullday, night
    course_name = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100), default='')
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=True)  # Course start date
    end_date = db.Column(db.Date, nullable=True)    # Course end date
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, classroom_id=0, day_of_week=0, shift='', course_name='', instructor='', start_time='', end_time='', start_date=None, end_date=None, is_active=True):
        self.classroom_id = classroom_id
        self.day_of_week = day_of_week
        self.shift = shift
        self.course_name = course_name
        self.instructor = instructor
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
    
    def __repr__(self):
        return f'<Schedule {self.course_name} - {self.shift}>'
    
    def to_dict(self):
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'day_of_week': self.day_of_week,
            'day_name': days[self.day_of_week],
            'shift': self.shift,
            'course_name': self.course_name,
            'instructor': self.instructor,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else '',
            'is_active': self.is_active
        }

class AdminSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    reporter_email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    hidden_from_classroom = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    admin_response = db.Column(db.Text)
    response_date = db.Column(db.DateTime)
    
    # Relationship with classroom
    classroom = db.relationship('Classroom', backref='incidents')
    
    def __init__(self, classroom_id=0, reporter_name='', reporter_email='', description=''):
        self.classroom_id = classroom_id
        self.reporter_name = reporter_name
        self.reporter_email = reporter_email
        self.description = description
        self.is_resolved = False
        self.hidden_from_classroom = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'classroom_name': self.classroom.name if self.classroom else 'Sala não encontrada',
            'reporter_name': self.reporter_name,
            'reporter_email': self.reporter_email,
            'description': self.description,
            'created_at': self.created_at.strftime('%d/%m/%Y às %H:%M') if self.created_at else '',
            'is_active': self.is_active,
            'is_resolved': self.is_resolved,
            'admin_response': self.admin_response,
            'response_date': self.response_date.strftime('%d/%m/%Y às %H:%M') if self.response_date else ''
        }
    
    def __repr__(self):
        return f'<Incident {self.id} - {self.reporter_name}>'

class ScheduleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    requester_name = db.Column(db.String(100), nullable=False)
    requester_email = db.Column(db.String(100), nullable=False)
    requester_phone = db.Column(db.String(20), default='')
    organization = db.Column(db.String(100), default='')
    event_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Schedule details
    requested_date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    shift = db.Column(db.String(20), nullable=False)  # morning, afternoon, fullday, night
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    
    # Bulk request support - for multiple dates
    additional_dates = db.Column(db.Text, default='')  # JSON string with additional dates
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_notes = db.Column(db.Text, default='')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(100), default='')
    
    # Relationship with classroom
    classroom = db.relationship('Classroom', backref='schedule_requests')
    
    def __init__(self, classroom_id=0, requester_name='', requester_email='', 
                 event_name='', description='', requested_date=None, 
                 day_of_week=0, shift='', start_time='', end_time='', additional_dates=''):
        self.classroom_id = classroom_id
        self.requester_name = requester_name
        self.requester_email = requester_email
        self.requester_phone = ''  # Keep for compatibility but not required
        self.organization = ''  # Keep for compatibility but not required
        self.event_name = event_name
        self.description = description
        self.requested_date = requested_date
        self.day_of_week = day_of_week
        self.shift = shift
        self.start_time = start_time
        self.end_time = end_time
        self.additional_dates = additional_dates
        self.status = 'pending'
    
    def to_dict(self):
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'classroom_name': self.classroom.name if self.classroom else 'Sala não encontrada',
            'requester_name': self.requester_name,
            'requester_email': self.requester_email,
            'event_name': self.event_name,
            'description': self.description,
            'requested_date': self.requested_date.strftime('%d/%m/%Y') if self.requested_date else '',
            'day_of_week': self.day_of_week,
            'shift': self.shift,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'additional_dates': self.additional_dates,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.strftime('%d/%m/%Y às %H:%M') if self.created_at else '',
            'reviewed_at': self.reviewed_at.strftime('%d/%m/%Y às %H:%M') if self.reviewed_at else '',
            'reviewed_by': self.reviewed_by
        }
    
    def __repr__(self):
        return f'<ScheduleRequest {self.id} - {self.event_name}>'
