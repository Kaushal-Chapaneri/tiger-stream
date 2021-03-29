<h1 align="center">TigerStream</h1>

<h2 align="center">

This Web-App is developed for the submission of <b>Build a Web-App with TigerGraph using Streamlit & Graphistry</b> <a style='text-decoration:none' target=_blank href=https://tigergraph-web-app-hack.devpost.com/>Hackathon</a>.

## Features

- Integration of TigerGraph database for Movie Recommendation starter-kit.
- Interactive Web application developed with Streamlit.
- Graph visualizations using Graphistry and Pyviz.

## Installed GSQL queries

- <b>UserStatistics</b>
	- Input : user id
	- Output : average rating, no. of movies rated, average rating, timestamp of rated movie

- <b>SimilarPeople</b>
	- Input : user id, no. of similar user
	- Output : similar movie list and similar movie count of N user's with respect to given user id

- <b>RecommendMovies</b>
	- Input : user id, no. of similar user, no. of movies to recommend
	- Output : list of movies along with their genre and other calculated matrices

## Streamlit features in action

- Multiple Page navigation
- Components for displaying saved html files and iframe
- Beta columns for side-by-side elements
- Plotly integration for interactive visualization
- DataFrame Pagination
- Tooltip on Hover 

## System Configurations

- This Project is developed and Tested with below mentioned system configurations.

```
- Operating System : Ubuntu 18.04 64 bit
- RAM : 4 GB
- Python version : 3.8.7
```

## Project setup

- Follow below steps to obtain necessary credentials. You can also watch videos of TigerGraph on [YouTube](https://www.youtube.com/playlist?list=PLq4l3NnrSRp7om_qw4ciNbxslMONszkoX) for these steps. 

```
- Login / Register on https://tgcloud.io/
- Create Solution using Movie Recommendation starter-kit, follow all default options.
- Once the solution is ready launch GraphStudio and sign in. 
- Generate secret token by heading to AdminPortal -> User Management
- Update config.json with tigergraph credentials.
- Login / Register on https://hub.graphistry.com/
- Update Graphistry credentials in config.json
```

- Visit all the pages on the left panel of GraphStudio and execute necessary steps.
- Copy GSQL queries present under asset/queries folder from this repo then go to Write Queries section in GraphStudio, create new query and paste there.
- Install all the queries in order to use them as API by clicking on Install all queries button.

## Environment setup

- Create virtual environment and install all the dependencies mentioned in requirements.txt

## Run project

```
- streamlit run TigerStream.py
```

## Linter
- [Flake8](https://realpython.com/python-pep8/#linters) extension available in VS Code is used to analyze code and flag errors.

## Demo
- Watch demo of this application on [YouTube](https://www.youtube.com/watch?v=lBdxM13H16Y).
