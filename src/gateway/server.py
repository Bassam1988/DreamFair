import os
import gridfs
import pika
import json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server=Flask(__name__)

mongo_video=PyMongo(
    server,
    uri= "mongodb://host.minikube.internal:27017/videos"             
    )
fs_videos=gridfs.GridFS(mongo_video.db)

mongo_mp3=PyMongo(
    server,
    uri= "mongodb://host.minikube.internal:27017/mp3s"             
    )
fs_mp3s=gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq",
        heartbeat=600,  # Heartbeat timeout in seconds
        blocked_connection_timeout=300
                                                               ))
channel=connection.channel()

@server.route("/login",methods=["POST"])
def login():
    token, err=access.login(request)

    if not err:
        return token
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err= validate.token(request)   
    if err:
        return err 
    access=json.loads(access)
    
    if access["admin"]:
        print("inside admin")
        if len(request.files)>1 or len(request.files)<1:
            return "exactly one file required", 400
        
        for _, f in request.files.items():
            print("inside for")
            err=util.upload(f,fs_videos,channel, access)
            print("after upload")
            if err:
                return str(err),500
        
        return "success", 200

    else:
        return "not authorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    access, err= validate.token(request) 
    if err:
        return err   
    access=json.loads(access)
    
    if access["admin"]:
        str_fid=request.args.get("fid")

        if not str_fid:
            return "fid is required", 400
        
        try:
            out=fs_mp3s.get(ObjectId(str_fid))
            return send_file(out, download_name=f"{str_fid}.mp3")
        except Exception as ex:
            print(ex)
            return "internal server error", 500

    return "not authorized", 401

if __name__=="__main__":
    server.run(host="0.0.0.0", port=8080)