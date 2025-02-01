docker build -t paperwallet .


docker run -it --rm -v $(pwd):/app paperwallet
