from model import Model


class Backend:
    def __init__(self, input_value):
        # Your machine learning model logic here
        self.model=Model()
        self.input=input_value
        self.model.generate_and_save_images(self.input)
        print( f"Prediction for {self.input}")
   
        