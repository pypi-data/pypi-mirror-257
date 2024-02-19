
import hashlib

import torch
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from skimage.io import imread
import numpy as np
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from torch.utils.data import DataLoader, Dataset, TensorDataset
import csv
import io as ioo
import uuid
from skimage import color
def privyml():
    print("This is the ml part of the programming.")
class _EncryptedFile(Dataset):
    def _derive_key(self, username, mac_address):
        # Combine username and MAC address
        combined_data = f"{username}:{mac_address}".encode('utf-8')
        salt = hashlib.sha256(combined_data).digest()
        # Derive a key using PBKDF2 with Argon2 as the underlying hash function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # Adjust the number of iterations according to your security requirements
            # salt=os.urandom(16),
            salt=salt,
            length=32
        )

        key = kdf.derive(combined_data)
        return key

    def get_mac_address(self):
        mac = uuid.getnode()
        return ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])

    def __init__(self, folder_path, datatype,username=None):
        self.folder_path = folder_path
        self.encryption_key = self._derive_key(username,self.get_mac_address())
        self.username = username
        self.dataType = datatype
        self.col_names = []
        self.file_list = [filename for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]

    def __len__(self):
        return len(self.file_list)

    def _parse_csv_data(self,csv_data):
        # Initialize lists to store features and labels
        features = []
        labels = []

        # Create a CSV reader from the CSV data
        csv_reader = csv.reader(ioo.StringIO(csv_data))
        # Iterate over rows in the CSV data
        info_row = True
        for row in csv_reader:
            if info_row:
                self.col_names = list(row)
                info_row = False
            else:

                # Assuming the first column contains features and the last column contains labels
                features.append(list(map(float, row[:-1])))  # Convert features to floats
                labels.append(int(row[-1]))  # Convert labels to integers

        labels = np.ravel(labels)
        # labels = np.array(labels)
        features_tensor = features
        labels_tensor = labels
        print(np.shape(features),"helllllllllll")
        print(np.shape(labels))
        return features_tensor, labels_tensor

    def __getitem__(self, idx):
        encrypted_file_path = os.path.join(self.folder_path, self.file_list[idx])
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Extract IV from the first 16 bytes
        iv = encrypted_data[:16]
        data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        if "csv" == self.dataType.lower():
            csv_string = ""
            try:
                csv_string = decrypted_data.decode("utf-8")
            except:
                csv_string +=""
            # Parse the CSV data and extract features and labels
            features, labels = self._parse_csv_data(csv_string)
            print(np.shape(features),np.shape(labels))
            return features, labels
        elif "image" == self.dataType.lower():
            # decrypted_image = self._decrypt_image(encrypted_data)
            decrypted_image = decrypted_data
            img = imread(ioo.BytesIO(decrypted_image))
            label = int(self.file_list[idx].split(".")[0])

            return img, label
        return decrypted_data

class _SecureDataLoader:
    def __init__(self, folder_path,datatype,username,batch_size = 1,shuffle = False):
        # self.encrypted_dataloader = encrypted_dataloader
        self.encrypted_dataset = _EncryptedFile(folder_path, datatype, username)
        self.X_train, self.y_train = zip(*_EncryptedFile(folder_path, datatype, username))
        print(np.shape(torch.Tensor(self.X_train)), "x_train")
        print(np.shape(self.y_train), "y_train")
        self.dataset = TensorDataset(torch.Tensor(np.squeeze(self.X_train)), torch.Tensor(np.squeeze(self.y_train)))
        print(self.dataset)
        self.encrypted_dataloader = iter(DataLoader(self.dataset, batch_size=batch_size, shuffle=shuffle))

    def __iter__(self):
        return self
    def __len__(self):
        return len(self.encrypted_dataloader)
    def __next__(self):
        encrypted_batch = next(self.encrypted_dataloader)
        # Process the encrypted batch further if needed, but don't expose decrypted data.
        return encrypted_batch

class customModal:
    def __init__(self, model,folder_path,datatype,username,batch_size = 1,shuffle = False):
        self.shuffle = shuffle
        self.model = model
        self.batch_size  = batch_size
        self.dataloader = _SecureDataLoader(folder_path,datatype,username,batch_size = self.batch_size,shuffle = False)
        self.data = [batch for batch in self.dataloader]
        print(self.data)
        self.X_train = []
        self.y_train = []
        if "csv"==datatype.lower():
            for batch in self.data:
                # Extend X_train with each feature tensor separately
                self.X_train.extend([value.numpy() for value in batch[0]])
                # Extend y_train with each label tensor
                self.y_train.extend(batch[1].numpy())
                # Convert lists to NumPy arrays
            self.X_train = np.array(self.X_train)
            self.y_train = np.array(self.y_train).reshape(-1, 1)
        elif "image"==datatype.lower():
            self.X_train = np.array([color.rgb2gray(value).flatten() for batch in self.data for value in batch[0]])
            self.y_train = np.array([value for batch in self.data for value in batch[1]]).reshape(-1, 1)

    def train_model(self):
        print(np.shape(np.squeeze(self.X_train)))
        # Training logic here
        self.model.fit(np.squeeze(self.X_train), self.y_train.reshape(-1,1))
        return self.model

    def predict(self,X_test = None):
        if X_test is None:
            self.X_test = [[1,2],[2,3]]
        else:
            self.X_test = np.array(X_test).flatten().reshape(1,-1)
            print(np.shape(np.array(X_test).flatten().reshape(1,-1)))
        # Prediction logic here
        return self.model.predict(self.X_test)

class customDlModel:
    def __init__(self,model,loss_function,optimiser,num_epochs,train_folder_path,test_folder_path,datatype,username,batch_size):
        self.model = model
        self.loss_function = loss_function
        self.optimiser = optimiser
        self.num_epochs = num_epochs
        self.train_folder_path = train_folder_path
        self.test_folder_path = test_folder_path
        self.username = username
        self.datatype = datatype
        self.batch_size = batch_size
        # self.X_train,self.y_train = zip(*_EncryptedFile(self.train_folder_path,self.datatype,self.username))
        # print(np.shape(torch.Tensor(self.X_train)),"x_train")
        # print(np.shape(self.y_train),"y_train")
        # self.dataset = TensorDataset(torch.Tensor(np.squeeze(self.X_train)),torch.Tensor(np.squeeze(self.y_train)))
        # print(self.dataset)
        self.train_loader = _SecureDataLoader(self.train_folder_path, self.datatype, self.username, self.batch_size, shuffle=False)
        self.test_loader =  _SecureDataLoader(self.test_folder_path, self.datatype, self.username, self.batch_size, shuffle=False)
        # self.train_loader = DataLoader(self.dataset,batch_size = 1,shuffle=False)
    def train_model(self):

        if self.datatype.lower() == "image":
            for epoch in range(self.num_epochs):
                running_loss = 0.0
                for images, labels in self.train_loader:
                    print(np.shape(images))
                    print(np.shape(labels))
                    labels = labels.long()
                    self.optimiser.zero_grad()
                    labels -= 1
                    images = images.permute(0, 3, 1, 2)
                    outputs = self.model(images.to(torch.float32))
                    loss = self.loss_function(outputs, labels)
                    loss.backward()
                    self.optimiser.step()
                    running_loss += loss.item()
                print(f"Epoch {epoch + 1}, Loss: {running_loss / len(self.train_loader)}")

            with torch.no_grad():
                correct = 0
                total = 0
                for images, labels in self.test_loader:
                    labels -= 1
                    images = images.permute(0, 3, 1, 2)
                    labels = labels.long()
                    outputs = self.model(images.to(torch.float32))
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                print(f"Accuracy: {100 * correct / total}%")
        elif self.datatype.lower() == "csv":
            for epoch in range(self.num_epochs):
                running_loss = 0.0
                print("lplplpl",len(self.train_loader))
                for features, labels in self.train_loader:
                    labels = labels.long()
                    print("here")
                    print(np.shape(features))
                    print(np.shape(labels))
                    print(np.shape(labels),"uhuhuhh")

                    self.optimiser.zero_grad()
                    # labels -= 1  # Adjust labels to start from 0
                    outputs = self.model(torch.tensor(features,dtype=torch.float32))
                    print(np.shape(outputs))
                    print(np.shape(labels))
                    print("jijijijiiijijiji",np.shape(labels))
                    loss = self.loss_function(outputs, labels)
                    loss.backward()
                    self.optimiser.step()
                    running_loss += loss.item()
                print(f"Epoch {epoch + 1}, Loss: {running_loss / len(self.train_loader)}")

            with torch.no_grad():
                correct = 0
                total = 0
                for features, labels in self.test_loader:
                    labels = labels.long()
                    outputs = self.model(features.to(torch.float32))
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                print(f"Accuracy: {100 * correct / total}%")


