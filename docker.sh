#!/bin/bash

if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
else
    RED=""; GREEN=""; YELLOW=""; BLUE=""; NC=""
fi

CONTAINER_NAME="test-ops-ia-container"
IMAGE_NAME="test-ops-ia"
PORT_MAPPING="8000:8000"
BUILD_PATH="."
DOCKERFILE="Dockerfile"
COPY_SOURCE_DEFAULT="/app/app/screenshots/"
COPY_DEST_DEFAULT="./imagenes_descargadas/"
COPY_SOURCE=""
COPY_DEST=""

print_success() { echo -e "${GREEN}[✓] $1${NC}"; }
print_error()   { echo -e "${RED}[✗] $1${NC}"; }
print_info()    { echo -e "${BLUE}[i] $1${NC}"; }

run_cmd() {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        print_error "Error ejecutando: $*"
        exit $status
    fi
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado o no está en PATH"
        exit 1
    fi
}

list_containers() { print_info "Listing all containers:"; docker ps -a; }

build_image() {
    print_info "Building image $IMAGE_NAME from $BUILD_PATH"
    run_cmd docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" "$BUILD_PATH"
    print_success "Image $IMAGE_NAME built successfully"
}

pull_image() {
    print_info "Pulling image $IMAGE_NAME"
    run_cmd docker pull "$IMAGE_NAME"
}

container_action() {
    local action=$1
    print_info "${action^} container $CONTAINER_NAME"
    run_cmd docker "$action" "$CONTAINER_NAME"
    print_success "Container $CONTAINER_NAME $action successfully"
}

run_container() {
    print_info "Running container $CONTAINER_NAME"
    run_cmd docker run -d -p "$PORT_MAPPING" --name "$CONTAINER_NAME" "$IMAGE_NAME"
    print_success "Container $CONTAINER_NAME started successfully (Ports: $PORT_MAPPING)"
}

exec_container() {
    print_info "Executing bash in container $CONTAINER_NAME"
    run_cmd docker exec -it "$CONTAINER_NAME" /bin/bash
}

show_logs() {
    print_info "Showing logs for container $CONTAINER_NAME"
    run_cmd docker logs "$CONTAINER_NAME"
}

clean_docker() {
    print_info "Cleaning unused resources"
    run_cmd docker system prune -f
    print_success "Cleanup completed"
}

copy_from_container() {
    local source_path="${COPY_SOURCE:-$COPY_SOURCE_DEFAULT}"
    local dest_path="${COPY_DEST:-$COPY_DEST_DEFAULT}"

    print_info "Copying from container $CONTAINER_NAME: $source_path -> $dest_path"
    mkdir -p "$dest_path"
    run_cmd docker cp "$CONTAINER_NAME:$source_path" "$dest_path"
    print_success "Files copied successfully"
    print_info "Source: $source_path"
    print_info "Destination: $dest_path"
    echo -e "${YELLOW}Contents of destination directory:${NC}"
    ls -la "$dest_path"
}

show_help() {
    cat << EOF
${GREEN}Usage: ./docker.sh [OPTIONS]${NC}

Options:
  -l, --list           List all containers
  -r, --run            Run container in background
  -s, --start          Start existing container
  -S, --stop           Stop container
  -b, --build          Build image
  -e, --exec           Execute bash inside container
  -L, --logs           Show container logs
  -p, --pull           Pull image
  -R, --remove         Remove container
  -ri, --remove-image  Remove image
  -c, --clean          Clean unused containers/images
  -cp, --copy          Copy files from container to host
  -n, --name NAME      Specify container name (default: $CONTAINER_NAME)
  -i, --image IMAGE    Specify image name (default: $IMAGE_NAME)
  -P, --port PORT      Specify port mapping (default: $PORT_MAPPING)
  -bp, --build-path PATH Build path (default: $BUILD_PATH)
  -f, --file FILE      Dockerfile to use (default: $DOCKERFILE)
  -cs, --copy-source   Source path in container (default: $COPY_SOURCE_DEFAULT)
  -cd, --copy-dest     Destination path on host (default: $COPY_DEST_DEFAULT)
  -h, --help           Show this help
EOF
}

check_docker

if [ $# -eq 0 ]; then show_help; exit 0; fi

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--list) list_containers ;;
        -r|--run) run_container ;;
        -s|--start) container_action start ;;
        -S|--stop) container_action stop ;;
        -b|--build) build_image ;;
        -e|--exec) exec_container ;;
        -L|--logs) show_logs ;;
        -p|--pull) pull_image ;;
        -R|--remove) container_action rm ;;
        -ri|--remove-image) run_cmd docker rmi "$IMAGE_NAME"; print_success "Image $IMAGE_NAME removed" ;;
        -c|--clean) clean_docker ;;
        -cp|--copy) copy_from_container ;;
        -n|--name) CONTAINER_NAME="$2"; shift ;;
        -i|--image) IMAGE_NAME="$2"; shift ;;
        -P|--port) PORT_MAPPING="$2"; shift ;;
        -bp|--build-path) BUILD_PATH="$2"; shift ;;
        -f|--file) DOCKERFILE="$2"; shift ;;
        -cs|--copy-source) COPY_SOURCE="$2"; shift ;;
        -cd|--copy-dest) COPY_DEST="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) print_error "Unknown option: $1"; show_help; exit 1 ;;
    esac
    shift
done
