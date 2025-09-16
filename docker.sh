#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CONTAINER_NAME="test-ops-ia-container"
IMAGE_NAME="test-ops-ia"
PORT_MAPPING="8000:8000"
BUILD_PATH="."
DOCKERFILE="Dockerfile"

COPY_SOURCE_DEFAULT="/app/app/screenshots/"
COPY_DEST_DEFAULT="./imagenes_descargadas/"

show_help() {
    echo -e "${GREEN}Usage: ./docker.sh [OPTIONS]${NC}"
    echo ""
    echo "Options:"
    echo "  -l, --list           List all containers (docker ps -a)"
    echo "  -r, --run            Run container in background"
    echo "  -s, --start          Start existing container"
    echo "  -S, --stop           Stop container"
    echo "  -b, --build          Build image"
    echo "  -e, --exec           Execute bash inside container"
    echo "  -L, --logs           Show container logs"
    echo "  -p, --pull           Pull image"
    echo "  -R, --remove         Remove container"
    echo "  -ri, --remove-image  Remove image"
    echo "  -c, --clean          Clean unused containers and images"
    echo "  -cp, --copy          Copy files from container to host (uses defaults)"
    echo "  -n, --name NAME      Specify container name (default: $CONTAINER_NAME)"
    echo "  -i, --image IMAGE    Specify image name (default: $IMAGE_NAME)"
    echo "  -P, --port PORT      Specify port mapping (default: $PORT_MAPPING)"
    echo "  -bp, --build-path PATH Build path (default: $BUILD_PATH)"
    echo "  -f, --file FILE      Dockerfile to use (default: $DOCKERFILE)"
    echo "  -cs, --copy-source   Source path in container (default: $COPY_SOURCE_DEFAULT)"
    echo "  -cd, --copy-dest     Destination path on host (default: $COPY_DEST_DEFAULT)"
    echo "  -h, --help           Show this help"
    echo ""
    echo "Copy examples:"
    echo "  ./docker.sh --copy                                  # Usa rutas por defecto"
    echo "  ./docker.sh -cp                                     # Usa rutas por defecto"
    echo "  ./docker.sh --copy --copy-source /app/screenshots/ --copy-dest ./descargas/"
    echo "  ./docker.sh -cp -cs /app/data/ -cd ./local_data/"
    echo ""
    echo "Current default copy paths:"
    echo "  Source (container): $COPY_SOURCE_DEFAULT"
    echo "  Destination (host): $COPY_DEST_DEFAULT"
}

print_success() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[i] $1${NC}"
}

list_containers() {
    print_info "Listing all containers:"
    docker ps -a
}

build_image() {
    print_info "Building image $IMAGE_NAME from $BUILD_PATH"
    docker build -t $IMAGE_NAME -f $DOCKERFILE $BUILD_PATH
    if [ $? -eq 0 ]; then
        print_success "Image $IMAGE_NAME built successfully"
    else
        print_error "Error building image"
        exit 1
    fi
}

pull_image() {
    print_info "Pulling image $IMAGE_NAME"
    docker pull $IMAGE_NAME
}

run_container() {
    print_info "Running container $CONTAINER_NAME"
    docker run -d -p $PORT_MAPPING --name $CONTAINER_NAME $IMAGE_NAME
    if [ $? -eq 0 ]; then
        print_success "Container $CONTAINER_NAME started successfully"
        print_info "Ports mapped: $PORT_MAPPING"
    else
        print_error "Error running container"
        exit 1
    fi
}

start_container() {
    print_info "Starting container $CONTAINER_NAME"
    docker start $CONTAINER_NAME
    if [ $? -eq 0 ]; then
        print_success "Container $CONTAINER_NAME started successfully"
    else
        print_error "Error starting container"
        exit 1
    fi
}

stop_container() {
    print_info "Stopping container $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    if [ $? -eq 0 ]; then
        print_success "Container $CONTAINER_NAME stopped successfully"
    else
        print_error "Error stopping container"
    fi
}

exec_container() {
    print_info "Executing bash in container $CONTAINER_NAME"
    docker exec -it $CONTAINER_NAME /bin/bash
}

show_logs() {
    print_info "Showing logs for container $CONTAINER_NAME"
    docker logs $CONTAINER_NAME
}

remove_container() {
    print_info "Removing container $CONTAINER_NAME"
    docker rm $CONTAINER_NAME
    if [ $? -eq 0 ]; then
        print_success "Container $CONTAINER_NAME removed successfully"
    else
        print_error "Error removing container"
    fi
}

remove_image() {
    print_info "Removing image $IMAGE_NAME"
    docker rmi $IMAGE_NAME
    if [ $? -eq 0 ]; then
        print_success "Image $IMAGE_NAME removed successfully"
    else
        print_error "Error removing image"
    fi
}

clean_docker() {
    print_info "Cleaning unused resources"
    docker system prune -f
    print_success "Cleanup completed"
}

copy_from_container() {
    local source_path="${COPY_SOURCE:-$COPY_SOURCE_DEFAULT}"
    local dest_path="${COPY_DEST:-$COPY_DEST_DEFAULT}"
    
    print_info "Copying from container $CONTAINER_NAME: $source_path to $dest_path"
    
    mkdir -p "$dest_path"
    
    docker cp $CONTAINER_NAME:$source_path $dest_path
    
    if [ $? -eq 0 ]; then
        print_success "Files copied successfully from container"
        print_info "Source: $source_path"
        print_info "Destination: $dest_path"
        
        echo -e "${YELLOW}Contents of destination directory:${NC}"
        ls -la "$dest_path"
    else
        print_error "Error copying files from container"
        print_info "Check if container is running and paths are correct"
        print_info "Container source: $source_path"
        print_info "Host destination: $dest_path"
        exit 1
    fi
}

if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

LIST=false
RUN=false
START=false
STOP=false
BUILD=false
EXEC=false
LOGS=false
PULL=false
REMOVE=false
REMOVE_IMAGE=false
CLEAN=false
COPY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--list)
            LIST=true
            shift
            ;;
        -r|--run)
            RUN=true
            shift
            ;;
        -s|--start)
            START=true
            shift
            ;;
        -S|--stop)
            STOP=true
            shift
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -e|--exec)
            EXEC=true
            shift
            ;;
        -L|--logs)
            LOGS=true
            shift
            ;;
        -p|--pull)
            PULL=true
            shift
            ;;
        -R|--remove)
            REMOVE=true
            shift
            ;;
        -ri|--remove-image)
            REMOVE_IMAGE=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -cp|--copy)
            COPY=true
            shift
            ;;
        -n|--name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE_NAME="$2"
            shift 2
            ;;
        -P|--port)
            PORT_MAPPING="$2"
            shift 2
            ;;
        -bp|--build-path)
            BUILD_PATH="$2"
            shift 2
            ;;
        -f|--file)
            DOCKERFILE="$2"
            shift 2
            ;;
        -cs|--copy-source)
            COPY_SOURCE="$2"
            shift 2
            ;;
        -cd|--copy-dest)
            COPY_DEST="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ "$CLEAN" = true ]; then clean_docker; fi
if [ "$PULL" = true ]; then pull_image; fi
if [ "$BUILD" = true ]; then build_image; fi
if [ "$RUN" = true ]; then run_container; fi
if [ "$START" = true ]; then start_container; fi
if [ "$STOP" = true ]; then stop_container; fi
if [ "$LIST" = true ]; then list_containers; fi
if [ "$LOGS" = true ]; then show_logs; fi
if [ "$EXEC" = true ]; then exec_container; fi
if [ "$REMOVE" = true ]; then remove_container; fi
if [ "$REMOVE_IMAGE" = true ]; then remove_image; fi
if [ "$COPY" = true ]; then copy_from_container; fi
