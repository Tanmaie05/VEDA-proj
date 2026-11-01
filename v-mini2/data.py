
# data.py
# Sample data for Veda Technology Business & Service Management System

services = [
    {
        "id": 1,
        "name": "Web Development",
        "category": "IT Services",
        "price": 15000,
        "status": "Active"
    },
    {
        "id": 2,
        "name": "Python Programming Training",
        "category": "Training",
        "price": 5000,
        "status": "Active"
    },
    {
        "id": 3,
        "name": "Cloud Computing",
        "category": "IT Services",
        "price": 12000,
        "status": "Active"
    }
]

programs = [
    {
        "id": 1,
        "name": "Python Programming",
        "duration": "4 Weeks",
        "category": "Technical Training",
        "status": "Open"
    },
    {
        "id": 2,
        "name": "Web Development Bootcamp",
        "duration": "6 Weeks",
        "category": "Technical Training",
        "status": "Open"
    },
    {
        "id": 3,
        "name": "Internship Program",
        "duration": "8 Weeks",
        "category": "Internship",
        "status": "Open"
    }
]

inquiries = [
    {
        "id": 1,
        "customer": "Ananya Rao",
        "subject": "Python Training",
        "message": "Interested in joining Python training.",
        "status": "New"
    },
    {
        "id": 2,
        "customer": "Rahul Sharma",
        "subject": "Web Development",
        "message": "Requesting details about web development services.",
        "status": "In Progress"
    }
]

service_requests = [
    {
        "id": 1,
        "customer": "Kiran Patil",
        "service": "Web Development",
        "description": "Website maintenance request.",
        "priority": "Medium",
        "status": "Open"
    },
    {
        "id": 2,
        "customer": "Meera Joshi",
        "service": "Cloud Computing",
        "description": "Cloud setup consultation.",
        "priority": "High",
        "status": "In Progress"
    }
]
