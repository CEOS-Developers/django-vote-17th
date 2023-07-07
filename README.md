# django-vote-17th
- `develop` : 현재 개발이 완료된 상태와 일치하는 branch 입니다. 🍒
- `master` / `main` : 현재 production 의 상태와 일치하는 branch 입니다. 🍒
- `feature` : `develop` 을 현재 개발 완료 상태와 일치시키면서 **다른 동료와 conflict가 생기지 않도록** 작업하기 위해 사용하는 branch 입니다. 🍒
- `release` : release 준비를 시작한 뒤, `develop` 에 merge한 **다음 release feature 로부터 안전한 release를 하기 위해** 사용하는 branch입니다.
- `hotfix` : `develop` **과 독립적으로** production에서 발생한 문제를 `master` 에서 처리하기 위해 사용하는 branch 입니다.
---
# 🛠️ **마지막 과제**

### **17기 파트장 및 데모데이 투표 서비스**

## 필수 기능

### 1. 로그인

- 사용자 로그인 여부는 JWT를 통해 인증합니다.
- 아이디 혹은 비밀번호가 틀렸을 시에는 에러를 반환합니다.
- (Optional) 로그아웃 기능
- [참고자료](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)

### 2. 회원가입

- 회원가입에 필요한 필드는 **아이디**, **비밀번호**, **이메일, 파트, 이름, 팀**입니다.
- **아이디, 이메일**은 중복될 수 없습니다. 
회원가입 과정 중에 중복 체크는 자유롭게 하셔도 됩니다.
    
    (중복체크 API를 따로 제작 혹은 회원가입 완료 시에 한 번에 체크)
    
- **파트**는 (프론트엔드, 백엔드) 중 하나를 선택할 수 있게 해주시면 됩니다.
- **팀**은 (RePick, 바리바리, Hooking, Dansupport, TherapEse) 중 하나를 선택할 수 있게 해주시면 됩니다.

### 3. 투표

- 후보는 득표 순으로 **내림차순 정렬**되어 보여집니다
- 투표 방법에 대해서는 제약이 없습니다. 한 아이디당 한 번만 투표하게 만드셔도 좋고, 투표 버튼 누르는 대로 득표수가 올라가도 상관없습니다.
- 로그인하지 않은 사용자는 투표 페이지에 접근할 수는 있되, 투표는 불가능합니다.
- **파트장 투표** : 본인의 파트에 해당하는 파트장 투표만 할 수 있습니다.
- **데모데이 투표** : 본인이 속한 팀을 제외하고 투표를 할 수 있습니다.

### 4. 기타

- 이외의 것들은 자유롭게 개발하시면 됩니다 😃

## 개발 환경 세팅

- 팀별로 **organization** 생성
- 미션 레포지토리를 organization으로 `fork`
    - 백엔드 미션 레포: [https://github.com/CEOS-Developers/django-vote-17th](https://github.com/CEOS-Developers/django-vote-17th)
- fork한 레포지토리를 `clone`후 작업

## 과제 제출

- 과제 완료 후 프로젝트의 변경사항을 fork한 자신의 remote repository에 push합니다.
- push를 완료했다면 자신의 repository에서 pull request를 진행합니다.
- **[프론트]** PR 제목은 [7주차] **팀이름** 미션 제출합니다 로 설정해 주세요.
- **[백엔드]** PR 시 내 팀 master 브랜치 → 내 팀 브랜치를 선택한 후, 메세지 제목은 [17기 팀이름] django-vote 미션 제출합니다 로 설정합니다.

## 과제 마감일

2023년 6월 28일

## 과제 최종 발표일

2023년 6월 30일

---
[정리](https://jain5379.tistory.com/33)