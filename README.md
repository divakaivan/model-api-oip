# 7/dockerise-start

The time has come for us to Dockerise our app so that the image can be used by whomever needs it and deployed.

### Dockerfile

Try to create a Dockerfile that

- builds uses a python image,
- copies the requirements.txt and installs the dependencies, and
- runs the api

Try to use a smaller Docker image. The smaller the image, the faster it will build and deploy, and it will also require less memory and disk space on the computer or container running it. You can start with the base python docker image, make sure everything runs and then try to slim down by using a smaller python image, and also you can try adding a `.dockerignore` to ignore files that are not needed for the app to run. To check the image sizes you can look at Docker desktop, or the terminal when building your image. For the python image sizes you can check the [python Docker hub repository](https://hub.docker.com/_/python/tags).

### Build and Push an image of our app to Docker Hub

Docker Hub is a repository for docker images. Try to add a new job into your github action to setup docker, login to docker hub, build and push your image to docker hub. Again, as before, to learn how to do these, you can google "github action login to docker hub", etc.

----------------

This is the end ~ We've come a long way :party:

For the final version, and most up-to-date check the main branch of my repo, and if you have any questions, want to improve this, let me know!

If you reached this far - thank you. I hope you learned at least a few good things and that I got you into the habit of reading documentation.
