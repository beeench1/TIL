### Git이란???

- 분산 버전 관리 시스템
- 코드의 히스토리(버전) 관리
- 개발되어온 과정 파악 가능
- 이전 버전과의 변경 사항 비교 및 분석
- 변경 사항만을 저장
- Git : 시스템 GitHub : 저장소
- Git은 명령어(CLI : Command-Line Interface)를 통해서 사용

![image-20210909103632662](C:/Users/dabee/AppData/Roaming/Typora/typora-user-images/image-20210909103632662.png)

### UNIX / LINUX 명령어

- ls : 해당 위치 폴더 파일 목록
- cd path : 경로 이동,
- cd . . : 상위폴더 이동
- mkdir dir.name : 폴더 생성
- touch file.name : 파일생성
- rm file.name : 삭제(파일만 가능)
- rm -r dir.name : 폴더 삭제

### 커밋(Commit)

: 특정 버전으로 남긴다. 3가지 영역에서 동작

1. Working Directory : 작업 공간
2. Staging Area : 커밋으로 남기고 싶은, 특정 버전으로 관리하고 싶은 파일이 있는 곳
3. Repository : 커밋들이 저장되는 곳 = sum(Committed file)

`(git init)` ->

Working Directory(Untracked) -> `(git add) `

-> Staging Area(Staged) -> `(git commit -m) `

-> Repository(Committed) 

Modify -> Working Directory(Modified) -> ` git add` -> `git commit -m`





### Git 명령어

git init : 로컬 저장소를 생성 

git status : 관리되고 있는 파일들 상태 체크

git add . : untracked 파일->tracked, Staging Area에 업로드

git commit -m : 커밋 (-m : 커밋 메세지, 작업 내용에 대한 주석)

git log : 전체 커밋g의 목록

git config --global user.name "user_name"

git config --global user.email "user_email"  : 이메일, 네임 전역 설정

git diff "ID" "ID" : 두 commit간 차이 보기(ID : 첫 4글자)

git remote add origin "github url"

git push -u origin master : 로컬에 있는 master의 변경 사항을 origin으로 넣기(온라인과 연결)

​											origin = remote repository 

git clone {repo_url} : remote_repo를 local로 복사(**from** remote_repo **to** local)

git clone {repo_url} . : 폴더 생성안하고 파일만 복사해옴   **.** 은 현재 디렉토리를 의미

git push origin master : **from** local **to** remote_repo

git pull origin master : **Get** repository change things **from** repository **to** Local **/** repository change things

git remote rm origin : origin 삭제

git restore --staged {file} : add 취소하기

git restore {file} : Working Directory 변경사항 취소하기

git reset --hard {c_id} : 커밋 되돌리기

.gitignore :  제외할 파일 / 폴더 만들기

​					디렉토리에 ".gitignore" 파일 만들고(touch .gitigore), 제외할 파일명, ''폴더명/'' 적기

  				 특정 파일 - 파일명

​                    특정 폴더 - 폴더명/

​					# 특정 확장자 제외 *.확장자(ex_ *.png / *.jpg)

​			

## 브랜치

git branch : 브랜치 목록

git branch {branch name} : 브랜치 생성

git checkout {branch name} : 브랜치이동

git merge {branch name} : 브랜치 병합, branch_name = 병합할 지점의 브랜치 이름

fast-forward merge : merge(t1,t2) = t2

git log --graph --oneline : 브랜치에 대한 로그 한줄씩 출력

git branch -t {branch url}

git branch -r 브랜치 전체 목록



#### Fork

**:** **from** other remote **to** my remote

​		(clone : **from** remote **to** local)

#### Process of Fork

Fork Opensource (**From** Remote **to** my remote)

 -> Clone to my local

 -> Add Branch & Update contents(At Local)

 ->  git push origin {branch name}

 ->  Pull request to Opensource repo



브랜치 업데이트

git rermote
