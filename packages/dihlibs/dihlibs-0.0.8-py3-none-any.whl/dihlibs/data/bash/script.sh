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

function deploy_cron() {
    file="${1%/}"
    folder="${file%.zip.enc}"
    [ -d "$file" ] || decrypt "$file" <.env
    user="$(yq .dih_user -r <"$folder"/config.yaml)"
    cron_time="$(yq .cronies.cron_time -r <"$folder"/config.yaml)"
    encrypt "$folder" <.env
    proj="${PWD##*/}"

    for x in {.cache,sql,$file}; do
        docker cp ./$n "dih-cronies:/dih/cronies/${proj}"
    done
    docker exec -i dih-cronies bash <<-CMD
        id -u $user || useradd -m -s /bin/bash -g dih $user
        chown -R $user /dih/cronies/${proj}
        runuser -u $user -- bash -c "{ crontab -l; echo '$cron_time' run "${proj}" ${file} ; } | crontab - "
CMD

    echo done deployment of $proj
}

# function remove_cron() {
#     file="${1%/}"
#     folder="${file%.zip.enc}"
#      || decrypt "$file" <.env
#     user="$(yq .user -r <"$folder"/config.yaml)"
#     cron_time="$(yq .cron_time -r <"$folder"/config.yaml)"
#     encrypt "$folder" <.env
#     proj=$(dirname .env)

#     docker exec -u "$user" dih-cronies bash -c 'crontab -l | grep -vE "\b'"$1"'\$" | crontab -' &&
#         docker exec dih-cronies rm -r "$folder"
# }

function perform() {
    case $1 in
    deploy) deploy_cron $2 ;;
    encrypt) encrypt $2 ;;
    decrypt) decrypt $2 ;;
    logs) docker-compose -f $2 logs -f & ;;
    down) docker-compose -f $2 down ;;
    stop) docker ps | grep "$2" | awk '{print $1}' | xargs docker stop ;;
    rm) docker container ls -a | awk '{print $1}' | xargs docker stop | xargs docker rm ;;
    esac
}

function create_shared_docker_resources() {
    docker network create --subnet=172.10.16.0/24 dih-network 2>/dev/null
    docker volume create dih-common 2>/dev/null
}
