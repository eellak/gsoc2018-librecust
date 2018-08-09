# The how to create an apt repo guide for normal people

## Generate key

gpg --full-generate-key

## List keys 

gpg --list-secret-keys --keyid-format LONG

```
gpg --list-secret-keys --keyid-format LONG
/Users/hubot/.gnupg/secring.gpg
------------------------------------
sec   4096R/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
uid                          Hubot 
ssb   4096R/42B317FD4BA89E7A 2016-03-10
```

3AA5C.... is the key $ID

## Export private key 

ID is the key id 
gpg --export-secret-keys $ID > my-private-key.key

## Export public key

gpg --armor --export $ID > mykey.pub

## Construct the repo directory
The repo should at least contain a conf folder and especially a file named distributions in it.

```bash
mkdir -p repo/apt/debian
cd repo/apt/debian
mkdir conf
```

Then create the conf/distributions file with the following content
```
Origin: Librecust
Label: librecust
Codename: precise
Suite: stable
Architectures: i386 amd64 source
Components: main
SignWith: librecust
```

General info about debian repositories [here](https://wiki.debian.org/DebianRepository)

## How to delete a deb from repo

```bash
reprepro remove [codename] [deb_name]
```

## How to add a deb to repo

```bash
reprepro includedeb [codename] [deb_name/path]
```

