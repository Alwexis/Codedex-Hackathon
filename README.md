# WaveNet
WaveNet is a 90s-inspired retro social network designed during a hackathon. The project draws heavy inspiration from the [MegaMan StarForce video game series](https://megaman.fandom.com/wiki/Mega_Man_Star_Force_(series)), blending retro aesthetics with a unique and engaging way to connect users. The goal was to replicate the simplicity, charm, and functionality of early internet technology while incorporating the concept of digital bonds central to MegaMan StarForce.

&nbsp;

## Inspiration
WaveNet draws its inspiration from the [MegaMan StarForce series](https://megaman.fandom.com/wiki/Mega_Man_Star_Force_(series)), where characters connected and shared information using portable devices called "[BrotherBands](https://megaman.fandom.com/wiki/BrotherBand)." These devices enabled users to form deep connections and access unique content through encrypted file sharing. **WaveNet** reimagines this concept for a social network by introducing the `.wavebond` system, where users generate and share encrypted files to add friends.

This design not only took inspiration from the 90s but also celebrates the futuristic imagination of that era, combining vibrant visuals, pixelated graphics, and simple, effective interfaces.

&nbsp;

## Key Features
### - Retro Design:
A user interface that replicates the look and feel of 90s-era technology, with bold colors, pixelated visuals, and period-appropriate graphical elements.
&nbsp;
### - Social Connections:
Users can create accounts, share posts, and interact with their friends through likes, comments, and private messages.
&nbsp;
### - Friendship via Encrypted Files:
A unique "WaveBond" system allows users to add friends by sharing and uploading `.wavebond` files.
&nbsp;
### - Private Messaging:
An inbox system enables real-time chat with friends, maintaining the retro-style experience.
&nbsp;
### - Posts and Interactions:
Share thoughts, engage with friends' posts and like on shared content to foster a connected community.

&nbsp;

## How WaveNet Works
### 1. Create an Account:
Sign up with a username, email, password and an optional profile picture.
&nbsp;
### 2. Generate a `.wavebond` File:
After registration, an encrypted `.wavebond` file unique to your account is generated. This file is used to share your profile with others.
&nbsp;
### 3. Add Friends:
To add a friend, insert (upload) their `.wavebond` file. WaveNet securely decrypts the file to establish the connection.
&nbsp;
### 4. Explore the Network:
- Post updates and like friends' posts.
- Chat privately with friends through the inbox feature.

&nbsp;

## How to Run the Project Locally
### Clone the repository:
```bash
git clone https://github.com/Alwexis/Codedex-Hackathon.git
```
&nbsp;
### Navigate to the project directory:
```bash
cd Codedex-Hackathon
```
&nbsp;
## How to Start the Backend and Frontend
### Backend
1. Ensure you have Python installed on your system.
2. Create a virtual enviroment
```bash
python -m venv .dev
```
3. Activate the virtual enviroment
```sh
cd .dev/Scripts/
.\activate
```
4. Install requirements
```sh
cd ../..
pip install -r requirements.txt
```
5. Start the FastAPI APP
```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Now the backend will be running at http://localhost:8000.
&nbsp;
### Frontend
1. Ensure you have Node.js installed on your system
2. Navigate to the frontend directory:
```sh
cd frontend
```
3. Install dependencies
```sh
npm install
```
4. Run app
```sh
npm run dev
```
The frontend will be available at http://localhost:5173/ (Probably).
