# PORTFOLIO APP
## Problem
There is need of developing a web application for users to showcase their work and update projects they have done with new ones while being able to track that which they've done.

## How to run this web application
* `git clone` this repository
* Open the folder using the `cd portfolio app`
* Navigate into the direct folder
* Run `npm install`
* `npm run dev` to display on your browser

## Tech used 
* React 
* TailwindCSS
* HTML
* JSFrontEnd

## Contributors
* Enock Kibet

## Features
The web application includes reusable project cards and a search bar. Together with an input form for entering new projects and also a project gallery where inputs are stored and past prjects.

## Components
**App** — Root component; manages projects state and search query; passes data to form and gallery
- **ProjectForm** — Form to add new projects; calls `onAdd` callback with `{title, description}`
- **ProjectGallery** — Wraps SearchBar and ProjectCard; displays filtered projects
- **SearchBar** — Controlled input; filters projects by query
- **ProjectCard** — Displays individual project title and description
