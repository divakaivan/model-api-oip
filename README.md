# 3/improve-docs-start

To improve the user experience by adding an example, I invite you to read this page from the FastAPI docs - [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/) and specifically the section about adding a `model_config` to pydantic models. 

Try to add a `model_config` field to the models that you think need an example. One case is like at the end of the last chapter - showing an example request body when using the inference endpoint. You can use the example I gave you in that previous readme as a guide. 

Another quality of life improvement would be adding tags. At the moment we see the word default above our endpoints. We can improve that by adding `tags` to our endpoints. I invite you to read this page on [Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/) and try to improve how our API looks.

Switch to `3/improve-docs-completed` whenever you think you can move on.