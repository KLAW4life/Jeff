from flask import Blueprint, request, jsonify, session
from bson import ObjectId
from datetime import datetime
from app.models import User, Patient, JournalEntry
# from app.chatbot import generate_response