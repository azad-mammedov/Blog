## Prerequisites

Before you begin, make sure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)


## Project Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone 
cd blog

docker build -t blog .
docker run -d -p 8000:8000 blog

Once the container is running, you can access the application in your web browser at:
http://localhost:8000
