#!/bin/bash

function trim() { sed -r 's/^\s*//g;s/\s*$//g'; }
function quiet() { "$@" &>/dev/null; }

function encrypt() {
    # Check for password input method
    echo "Enter password for encryption:"
    read -s password
    echo # Move to a new line for cleaner output

    if [ "$#" -ne 1 ]; then
        echo You must specify the file to encrypt
        return 1
    fi

    local file="${1%/}"
    local encrypt="$file.zip"
    quiet zip -r "$encrypt" "$file"
    # File name is provided, encrypt the file
    openssl enc -aes-256-cbc -pbkdf2 -iter 10000 -salt -in "$encrypt" -out "$encrypt.enc" -pass pass:"$password"
    [ "$?" -eq 0 ] && rm -rf "$file"
    rm "$encrypt"
}

function decrypt() {
    echo "Enter password for decryption:"
    read -s password
    echo # Move to a new line for cleaner output

    if [ "$#" -eq 1 ]; then
        local encrypted_file="$1"
        local file="${encrypted_file%.enc}"
        openssl enc -aes-256-cbc -d -pbkdf2 -iter 10000 -salt -in "$encrypted_file" -out "$file" -pass pass:"$password"
        [[ "$?" -ne 0 ]] && rm -rf "$file" && return 1
        [[ $file =~ \.zip$ ]] && quiet unzip "$file" && rm "$file" "$file.enc"
    fi
}

function strong_password() {
    trim <<-CODE | python
    import dihlibs.functions as fn
    print(fn.strong_password($1))
CODE
}

function turn_on_cron_container(){
    echo turning on dhis containers
    docker-compose -f .cache/docker/cronies/docker-compose.yml up -d 2>&1
}

function turn_on_dhis_containers(){
    echo turning on dhis containers
    docker-compose -f .cache/docker/backend/dhis/"$1"-compose.yml up -d 2>&1
}


function deploy_cron() {
    file="${1%/}"
    temp=$(mktemp -d)
    
    loc="$(dirname $file)"
    [[ $loc == "." ]] && loc=$PWD;
    proj="${loc##*/}"
    file=${file##*/}
    folder="${file%.zip.enc}"

    cp -r $loc/.* $loc/*  $temp/
    cd $temp

    [ -d "$file" ] || decrypt "$file" <.env
    user="$(yq .dih_user -r <"$folder"/config.yaml)"
    cron_time="$(yq .cronies.cron_time -r <"$folder"/config.yaml)"
    sed -ri "s/(dhis_url.*)localhost([^@]*$)?/\1${folder}-dhis:8080\2/g" "$folder/config.yaml"
    encrypt "$folder" <.env
    
    echo "local ni $loc"
    docker exec dih-cronies mkdir -p "/dih/cronies/${proj}"
    for x in {.cache,sql,$file,.env}; do
        docker cp ./$x "dih-cronies:/dih/cronies/${proj}"
    done
    docker exec -i dih-cronies bash <<-CMD
        id -u $user || useradd -m -s /bin/bash -g dih $user
        chown -R $user /dih/cronies/${proj}
        runuser -u $user -- bash -c "{ crontab -l; echo '$cron_time' run "${proj}" ${file} ; } | crontab - "
CMD

    rm -rf $temp

    echo done deployment of $proj
}

function perform() {
    case $1 in
    deploy) deploy_cron $2 ;;
    encrypt) encrypt $2 ;;
    decrypt) decrypt $2 ;;
    dhis-log*) docker-compose -f .cache/docker/backend/dhis/"${2%.zip.enc}"-compose.yml logs -f ;;
    cron-log*) docker-compose -f .cache/docker/cronies/docker-compose.yml logs -f ;;
    down) docker-compose -f $2 down ;;
    stop) docker ps | grep "$2" | awk '{print $1}' | xargs docker stop ;;
    rm) docker container ls -a | awk '{print $1}' | xargs docker stop | xargs docker rm ;;
    esac
}

function create_shared_docker_resources() {
    docker network create --subnet=172.10.16.0/24 dih-network 2>/dev/null
    docker volume create dih-common 2>/dev/null
}
