# ✦ MCF Teams Banner Generator
<p align="center">
  <img src="https://user-images.githubusercontent.com/66202304/160249081-1802ff23-3d7b-4ac3-af2c-6c5728c18f6d.png" width="960" />

  ## ★ A small python script we use to generate banners displaying the players participating.
</p>

#### • Step 1) Download Git Repo.
```
git clone https://github.com/NovaUniverse/MCF-Teams-Banner-Generator
```

#### • Step 2) Install all required dependencies.
```cmd
cd MCF-Teams-Banner-Generator
pip install -r requirements.txt
```

#### • Step 3) Run script and drag the teams.json file in the console.
```cmd
cd src
python run.py
```
![image](https://user-images.githubusercontent.com/66202304/160249424-11bc975c-6e42-43e0-8181-249f3b960f38.png)

#### • Step 4) DONE! The PNG should open up but it can also be found in the 'dest' folder with the following date.
![image](https://user-images.githubusercontent.com/66202304/160249393-a05f7ea4-dec1-4d2b-8e83-316df583e500.png)

## Command Line Args
*(Assuming your in the src directory.)*
```
python run.py {path to teams.json} {date: 10/04/2022} {max teams: 12} {open file: true/false}
```
#### To settle with default options you can just pass "none" or "null". Also we drop the final rendered images in a "dest" folder in the root directory.

**© Copyright (C) 2022 Nova Universe (Under the [GPL-3.0 License](LICENSE.md))**
