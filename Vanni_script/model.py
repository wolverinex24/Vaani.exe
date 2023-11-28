from datetime import datetime
import cv2
# from cv2 import dnn_superres
import os
import torch
import torchvision
from generator import Generator
from  config import config
from preprocessor import wordPreproccessor,preprocess_sentence,inverseWordpreproccessor
from gifGen import create_gif

class Model:
    
    
    upscale_directory=''
    device = "cuda" if torch.cuda.is_available() else print("running on cpu")
    # torch.cuda.set_device(device=0)
    Z_DIM = config["Z_DIM"]
    CHANNELS_IMG = config["CHANNELS_IMG"]
    FEATURES_GEN = config["FEATURES_GEN"]
    NUM_CLASSES = config["NUM_CLASSES"] # Number of classes for your custom dataset
    IMG_SIZE = config["IMG_SIZE"]
    GEN_EMBEDDING = config["GEN_EMBEDDING"]

    LEARNING_RATE = config["LEARNING_RATE"]
    BATCH_SIZE = config["BATCH_SIZE"]
    NUM_EPOCHS = config["NUM_EPOCHS"]
    FEATURES_CRITIC = config["FEATURES_CRITIC"]
    CRITIC_ITERATIONS = config["CRITIC_ITERATIONS"]
    LAMBDA_GP = config["LAMBDA_GP"]
    
    def __init__(self):
        # Load the saved generator model
        self.generator = Generator(self.Z_DIM, self.CHANNELS_IMG, self.FEATURES_GEN, self.NUM_CLASSES, self.IMG_SIZE, self.GEN_EMBEDDING).to(self.device)
        self.generator.load_state_dict(torch.load("Vanni_script\\generator.pth",map_location=torch.device('cpu')))
        self.generator.eval()  # Set the generator in evaluation mode

    


    # Function to generate images and save them with consistent timestamps
    def generate_and_save_images(self,input):
        # Get the timestamp for the current loop iteration
        loop_start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Create an SR object
        # sr = dnn_superres.DnnSuperResImpl_create()
        # # Set the desired model and scale to get correct pre- and post-processing
        # sr.setModel("edsr", 4)
        # path = "E:\\ml_start\\GAN_ISL\\archive\EDSR_x4.pb" #Give your specific path to SR model
        # sr.readModel(path)
        
        userInput=wordPreproccessor(preprocess_sentence(str(input)))

        
        for i in userInput:
            word = inverseWordpreproccessor(i).strip()  # Remove any leading/trailing whitespace
            # Specify the label you want to generate images for
            desired_label = torch.tensor([i]).to(self.device)

            # Generate random noise vectors (you can change the number of vectors)
            num_samples = len(desired_label)
            noise = torch.randn(num_samples, self.Z_DIM, 1, 1).to(self.device)

            print(f"GENERATING IMAGE {word}")
            # Generate images with the desired label
            with torch.no_grad():
                generated_images = self.generator(noise, desired_label)

            # Create a folder based on the loop start time
            output_directory = os.path.join("generated_images", loop_start_time)
            os.makedirs(output_directory, exist_ok=True)
            
            # Create a subfolder for upscaled images
            global upscale_directory
            upscale_directory = os.path.join(output_directory, f"{loop_start_time}_upscaled")
            os.makedirs(upscale_directory, exist_ok=True)

            # Find the latest sequential number in the folder
            files_in_folder = os.listdir(output_directory)
            sequential_number = len(files_in_folder)
            
            # Save the generated images with sequential names
            for idx,img in enumerate(generated_images):
                image_filename = os.path.join(output_directory, f"{sequential_number + idx}.png")
                torchvision.utils.save_image(img, image_filename, normalize=True)
                # Read image
                image = cv2.imread(image_filename)
            
                
                # result = sr.upsample(image) #using SR method 
                # cv2.resize(image,dsize=None,fx=4,fy=4)
                result = image
                
                # Generate the filename for the upscaled image
                upscale_image_filename = os.path.join(upscale_directory, f"{sequential_number+idx}.png")
                # Save the image
                cv2.imwrite(upscale_image_filename, result)
        

            
       
       

        directory_path = upscale_directory
        output_path = 'Vanni_script\\Gifoutput'
        os.makedirs(output_path, exist_ok=True)
        
        create_gif(directory_path, output_path) 
