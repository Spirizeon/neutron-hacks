FROM debian:bookworm
COPY . . 
EXPOSE 5000
RUN apt update
RUN apt install -y python3 python3-pip git
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --break-system-packages
RUN pip install -r requirements.txt --break-system-packages
CMD ["python3","app.py"]
