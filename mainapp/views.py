# views.py
import subprocess
import json
from django.http import JsonResponse
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FileUploadParser
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os

# yourapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
from PIL import Image
import json

from .utility import load_model

model_path = settings.DETECTION_MODEL  # Update with the correct path
model = load_model(model_path)

@csrf_exempt
def detect_objects(request):
    if request.method == 'POST':
        try:
            uploaded_image = Image.open(request.FILES['image'])
            confidence = float(request.POST.get('confidence', 0.4))
            results = model.predict(uploaded_image, conf=confidence)
            # print(results)
            # Process results as needed
            boxes = results[0].boxes
            names = results[0].names
            print(boxes)
            print(names)
            # print(boxes[0].cls)
            # print(names[int(boxes[0].cls[0])])

            detected_objects = []
            for box in boxes:
                detected_object = {
                    'xyxy': box.xyxy.tolist() if box.xyxy is not None else None,
                    'conf': box.conf.tolist() if box.conf is not None else None,
                    'cls': box.cls.tolist() if box.cls is not None else None,
                    'id': box.id.tolist() if box.id is not None else None,
                    'xywh': box.xywh.tolist() if box.xywh is not None else None,
                    'xyxyn': box.xyxyn.tolist() if box.xyxyn is not None else None,
                    'xywhn': box.xywhn.tolist() if box.xywhn is not None else None,
                    'class_name': names[int(box.cls[0])] if names is not None and box.cls is not None else None,

                }
                detected_objects.append(detected_object)

            return JsonResponse({'detected_objects': detected_objects}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)