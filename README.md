
**Chesstify Backend App**  
===  
  
This repository contains the backend APIs for Chesstify built in Python using Flask  
  
**Requirements**  
---  
To install and run this project you will need:  
- Python 3.7+  
  
Installation
---  
To start the project locally, do the following steps
  
-  Clone the project
 `git clone  [https://github.com/Chesstify/chesstify-backend.git]`
 
- Create a virtual environment
`python -m venv [envName]  `
  
- Then start up your new environment:  
   - **[Windows]** (Using powershell) :  `.\envName\Scripts\Activate.ps1`
	- **[Mac]**:    `source envName/bin/activate`  
  
- Once your virtual environment is running, make sure you are within the repository and install the necessary packages  
`pip install -r requirements.txt`

Running the Application
---

**[Windows]**

	set FLASK_APP=main/chesstify.py
	$env:FLASK_APP="main/chesstify.py"
	flask run
	
**[Mac]**

	export FLASK_APP=main/chesstify.py
	flask run


You should then see the following output
```
* Serving Flask app "main/chesstify.py"
* Running on http://127.0.0.1:5000/
```

