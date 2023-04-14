from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash

db = SQLAlchemy()

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    observation = db.Column(db.String(255))

    def __repr__(self):
        return f'<Device {self.imei}>'
