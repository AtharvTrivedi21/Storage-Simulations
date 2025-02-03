Extendible Hashing and Bitmap Indexing README File for instructions
24MCD002, 24MCD019

Please note that the files for Extendible Hashing are:
For API: ex_api,py and for App/Website: ex_app.py

And for BitMap Indexing:
For API: bit_api.py and for App/Website: bit_app.py

Steps:
1. Type the following commands in the terminal or command prompt to installed the required libraries:

pip install fastapi
pip install "uvicorn[standard]"
pip install pydantic
pip install streamlit
pip install requests
pip install watchdog

2. Now we need to create a virtual environment to run the python files, to do that type the following (Might need it the command prompt is used):

python -m venv myenv

myenv\Scripts\activate

3. Next step is to store the files in the folder where the above steps were performed (in the same place).

4. Lastly, we will need two terminals or two command prompts to do this since we have to start the API and then the StreamLit App. So, do the following:

- Type this in the first terminal:
uvicorn ex_api:app --reload
# this is to start the API

- In the other terminal type:
streamlit run ex_app.py
# this is for the app to be opened in a browser

The above 2 instructions will start the Extendible Hashing website running locally on a browser.

Similarly for BitMap Indexing:

- Type this in the first terminal:
uvicorn bit_api:app --reload
# this is to start the API

- In the other terminal type:
streamlit run bit_app.py
# this is for the app to be opened in a browser


