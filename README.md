# django-vote-17th
파트장/데모데이 투표

## ERD 구조

![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/638fbf23-20c9-4bb4-a563-ca82b050888b)

### 데이터셋
```json
insert into vote_team(created_at, updated_at, team, vote_cnt) values ("2023-06-15","2023-06-15","RePick",0);
insert into vote_team(created_at, updated_at, team, vote_cnt) values ("2023-06-15","2023-06-15","바리바리",0);
insert into vote_team(created_at, updated_at, team, vote_cnt) values ("2023-06-15","2023-06-15","Hooking",0);
insert into vote_team(created_at, updated_at, team, vote_cnt) values ("2023-06-15","2023-06-15","Dansupport",0);
insert into vote_team(created_at, updated_at, team, vote_cnt) values ("2023-06-15","2023-06-15","TherapEase",0);

insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","권가은","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","김문기","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","김서연","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","노수진","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","배성준","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","신유진","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","오예린","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","이예지","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","장효신","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","최민주","front",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","김지원","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","김현수","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","김현우","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","서찬혁","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","서혜준","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","이소정","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","임탁균","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","조예지","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","최유미","back",0);
insert into vote_candidate(created_at, updated_at, name, part, vote_cnt) values ("2023-06-15","2023-06-15","황재령","back",0);

```
## 기능 소개

### 주요 기능 목록
- 유저 관련 기능
    - 회원가입
    - 로그인
- 투표 관련 기능
    - 팀 투표
    - 파트장 투표

### 회원가입 
📤 Request
```json
{
  "user_id": "hk", //아이디
  "password": "qwe123", //비밀번호
  "email": "hook@naver.com", //이메일
  "part": "back", //속한 파트
  "name": "hook", //이름
  "team": "Hooking"  //팀 이름
}
```
cf. part 선택시, ‘back’과 ‘front’만 가능

📥 Response
```json
{
  "user_id": "hk", //아이디
  "email":"hook@naver.com", //이메일
  "part": "back", //속한 파트
  "name": "hook",  //이름
  "team": "Hooking"  //팀 이름
}
```
- 아이디, 이메일 중복체크는 API를 따로 만들지 않고, 회원가입이 완료될 때 한번에 체크되도록 구현했습니다. (중복 시 400 에러 반환)
- 회원가입할 때, 아이디 중복 시
![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/9694e657-bd5e-4394-9703-1a2dcecee1a9)
- 마찬가지로, 이메일 중복 시
![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/4cd0e476-8d70-4b87-a517-82dac52a7b4d)

### 로그인
📤 Request
```json
{
  "user_id": "hk", //아이디
  "password": "qwe123" //비밀번호
}
```
📥 Response
```json
{
    "user_id": "hk",
    "team": "Hooking",
    "part": "back",
    "token": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2ODMyMTI1LCJpYXQiOjE2ODY4MzE4MjUsImp0aSI6IjA1MDhmNzBmNDRhNjQzOGI4ZDgwOTYzZWZmY2RjNzFiIiwidXNlcl9pZCI6MX0.q_pi_JgVCha-SJLupzWWm5Z4TgIwqxJWA8KhraW0NwQ"
    }
}
```
- 로그인을 하면 access_token이 발급됩니다. 
- 이후에 투표 관련 API 접근 시 로그인 할 때 발급된 access_token 을 이용해 접근이 가능합니다. 
- 아이디 혹은 비밀번호가 틀렸을 시에는 로그인되지 않고 ERROR 메세지를 반환합니다. 
![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/cea54445-d535-4109-a8e3-bf4543d32037)

![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/381c3897-2f98-436c-885c-1704e675a711)

### 팀 투표하기
📤 Request
```json
{
	"user_name": "hook", //투표자 이름
	"team": 2 //투표팀 번호
}
```
📥 Response
```json
{
	"user_name": "hook", //투표자 이름
	"team": "바리바리", //투표팀 이름
	"team_cnt": 2 //투표팀 투표횟수
}
```
- 로그인한 사용자만 투표가 가능
- User의 `is_teamvote` 필드를 통해 투표 여부를 확인하고 해당 필드값이 `False`인 경우 즉, 투표를 하지 않은 사용자만 투표할 수 있게 구현하였습니다.
![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/ab76a541-413c-4df0-bf9b-14562dd58c50)

### 팀 투표 확인하기
- 득표 수를 기준으로 내림차순 정렬되어 보여집니다.
![image](https://github.com/Hooking-CEOS/Hooking_BE/assets/81136546/40cc8bce-a099-4ad1-b41c-bd4c6e5bdd72)

### 파트장 투표하기
📤 Request
```json
{
   "user_name": "hook", //투표자 이름
   "candidate": 2  //파트장 기본키
}
```
📥 Response
```json
{
   "user_name": "hook", //투표자 이름
   "candidate": 2, //파트장 기본키
   "candidate_cnt": 2  //투표횟수
}
```
- 로그인한 사용자만 투표 가능 
- User의 `is_partvote` 필드를 통해 투표 여부를 확인하고 해당 필드값이 `False`인 경우 즉, 투표를 하지 않은 사용자만 투표할 수 있게 구현하였습니다.
- 팀 투표 url에 part 명을 입력하여 해당 파트에 투표가 가능

### 파트장 투표 확인하기
- 득표 수를 기준으로 내림차순 정렬되어 보여집니다.

## 회고
- 지원: 간단한 토이프로젝트를 해보며 ERD 설계부터 배포까지 전체적인 흐름을 파악할 수 있어 좋았다. 저번 CEOS 백엔드 과제를 하며 ERD를 제대로 안짜면 잠을 못자며 작업을 해야한다는 사실을 깨달았기에, 신경써서 짰다. 또한, 프론트분들께 어떻게 하면 편하게 넘겨드릴지 고민을 많이 했다. 프론트 경험이 있어서 그런지 그 고생을 알기때문에... 아무튼 크게 문제될 것 없이 잘 흘러갔던 거 같아 뿌듯하다. 모두 수고하셨습니다😊!

- 예지: 규모가 큰 프로젝트는 아니었지만 우리 프론트팀과 처음 협업을 해서 완성된 서비스를 만들 수 있었던 좋은 경험이었습니다. 본 프로젝트를 진행하기 전에 워밍업 느낌으로 프론트분들과 어떤 식으로 소통을 해야하는지 깨달을 수 있었고, 이번 학기에 처음 접했던 장고이지만 한 학기동안 세오스 스터디를 열심히 하며 그래도 많이 익숙해진 것 같습니다! 스터디할 때 에러고치느라 힘들었던 배포 과정도 이번엔 큰 시행착오없이 넘어갈 수 있었어서 너무 행복했습니다. 앞으로 남은 우리 후킹 프로젝트도 화이팅^.^

