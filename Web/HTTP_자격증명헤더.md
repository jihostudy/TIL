## HTTP 자격증명 헤더

HTTP 자격증명 헤더는 클라이언트와 서버 간의 인증과정에서 사용자의 자격을 확인하기 위한 헤더 필드이다.

서버에서 헤더에 담아 클라이언트로 보내는 `WWW-Authenticate` 필드와

클라이언트에서 헤더에 담아 서버로 보내는 `Authorization` 필드가 있다.

큰 틀로는 다음 과정으로 진행된다.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/d5aad0fb-3105-4c8e-9d97-5f18b6a29f1d" />


1. 클라이언트가 웹 서버에 특정 서비스를 사용하기 위해 요청을 보낸다.
2. 웹 서버는 권한이 없는 클라이언트임을 확인하고, 401 `Unauthorized 상태코드`와 `WWW-Authenticate 필드`를 담아서 클라이언트에 보낸다.
3. 클라이언트는 받은 `WWW-Authenticate` 필드를 토대로 웹 서버가 필요한 정보를 제공한다.
4. 웹 서버는 인증을 성공한 유저를 인증해주고 리소스를 제공한다.

이때, 서버에서 제공하는 `WWW-Authenticate` 자격증명 헤더값의 Syntax는 다음과 같다. [(참고 자료)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate)

```
WWW-Authenticate: <challenge>

challenge = <auth-scheme> <auth-param>, …, <auth-paramN>
challenge = <auth-scheme> <token68>
```

auth-scheme (필수값): 인증 방식 ([`Basic`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#basic_authentication_scheme), `Digest`, `Negotiate` and `AWS4-HMAC-SHA256`  …)

example

```
WWW-Authenticate: Basic realm="Dev", charset="UTF-8"
```

그렇다면 인증 방식에는 무엇이 있는지 알아보겠다.

## 인증 방식

인증 방식은 기본 인증(Basic Authentication), 다이제스트 인증(Digest Authentication), 베어러 토큰 (Bearer Token) 방식 크게 총 3가지가 있다.

### 기본 인증 (Basic Authentication)

기본 인증 방식은 간단하게 인증할 때 사용하며, 보안 취약점이 존재하여 주의하여 사용해야 합니다.

사용자 이름과 비밀번호를 콜론(**`:`**)으로 구분하여 base64로 인코딩한 값을 **`Authorization`** 헤더에 포함하여 서버로 전송합니다.

예를 들어, 사용자 이름이 `user`이고 비밀번호가 `password`인 경우, 먼저 이를 **`user:password`** 형태로 결합한 후 base64로 인코딩하여 HTTP 요청에 포함합니다.

```jsx
GET /protected/resource HTTP/1.1
Host: example.com
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

형식 **`Authorization: <type> <credentials>`**

위 예시에서 `dXNlcjpwYXNzd29yZA==`는 `user:password`를 base64 인코딩한 값입니다.

<aside>
💡 base64란?

- 6비트 이진 데이터(예를 들어 실행 파일이나, ZIP 파일 등)를 문자 코드에 영향을 받지 않는 공통 **ASCII 영역**의 문자들로만 이루어진 일련의 **문자열**로 바꾸는 **인코딩** 방식
- 보안에 취약해서 HTTPS랑 같이 사용해야 한다.
</aside>

*특징*

- base64는 쉽게 디코딩될수 있으므로, HTTPS, TLS/SSL 환경에서 사용해야 합니다.
    - MITM(Man In The Middle) 공격자에 의해 쉽게 탈취됩니다.
- (OAuth만 사용하는 경우와 대비하여) 서버에 로그인 정보, 아이디와 패스워드를 직접 저장해야 합니다.
    - OAuth만 사용하는 경우와 비교했을때, 유저 정보를 보관하는 것은 똑같으나 유저의 아이디, 패스워드를 저장 및 탐색하는 저장 공간과 시간이 필요합니다.

<img width="614" alt="image" src="https://github.com/user-attachments/assets/e44812c5-aa9c-4595-926f-f71c5bec0e80" />

[토스페이먼츠에서 소개하는 Basic의 장단점](https://docs.tosspayments.com/resources/glossary/basic-auth)

### 다이제스트 인증 (Digest Authentication)

다이제스트 인증 방법은 기본 인증의 보안 취약점을 극복한 방법으로 사용자의 비밀번호를 직접 전송하지 않고 비밀번호의 해시된 버전을 사용합니다.

초기, `WWW-Authenticate` 헤더에 `nonce` 값과 `realm` 정보를 웹 서버는 포함하여 제공합니다.

<aside>
💡

nonce 값

`“Number used once”`의 약자로, 한 번만 사용되는 숫자로 난수를 의미합니다.

서버에서 임의로 생성되고 각 인증 요청마다 고유하게 발급합니다.

이를 받은 클라이언트는 해당 `nonce` 값을 인증 정보를 생성할 때 포함시켜야 하며, 서버는 이 값을 검증하여 동일한 인증 요청이 재사용되는 것을 방지합니다.

→ 재전송 공격 (replay attack)를 방지하기 위함입니다.

<aside>
💡

재전송 공격

말 그대로 MITM(중간자)가 요청을 가로채어 약간 변조하여 재전송하는 것을 의미한다.

난수는 한번만 사용될 수 있는 값이므로 재전송 공격의 요청은 무시된다.

</aside>

</aside>

<aside>
💡

realm 값

서버가 관리하는 인증 영역을 구분하는 데 사용되며, 리소스 영역을 식별하는 문자열입니다.

이는 사용자에게 어떤 영역이나 자원에 대해 인증이 요구되고 있는지 알려주는 역할을 합니다.

클라이언트는 이 `realm` 값을 인식하고, 적절한 자격 증명을 사용하여 인증을 시도합니다.

</aside>

서버

<img width="477" alt="image" src="https://github.com/user-attachments/assets/13e67830-f2ae-4534-aba7-b01368ff853e" />

클라이언트

<img width="507" alt="image" src="https://github.com/user-attachments/assets/943fe2ac-f45e-418f-9b3d-38fc56f69318" />

서버

<img width="585" alt="image" src="https://github.com/user-attachments/assets/ff46a55f-f1c7-4d8a-9253-957086d73ea2" />)=

이때, 비밀번호를 `md5` 해시 함수를 이용하여 암호화하여 보냅니다.

- md5는 암호학적으로 취약해서 현실에서 사용하지 않습니다.

<aside>
💡

MD5

MD5 (Message-Digest Algorithm 5)는 해시 함수로 사용되며, 주로 데이터 무결성 검증에 사용됩니다.

데이터나 파일의 내용을 입력받아 128비트 길이의 해시 값을 생성하는데, 이 해시 값은 입력된 데이터의 고유한 "지문" 역할을 합니다.

하지만 MD5는 암호학적으로 안전하지 않다고 알려져 있으며, 충돌 공격에 취약하다는 단점이 있습니다.

따라서 보안이 중요한 애플리케이션에서는 MD5 대신 더 안전한 해시 알고리즘을 사용하는 것이 권장됩니다.

</aside>

코드예시

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Digest realm="example.com",
                  nonce="abc123",
                  qop="auth",
                  algorithm=MD5
```

```
HA1 = MD5(username:realm:password)
HA2 = MD5(method:URI)
response = MD5(HA1:nonce:HA2)
```

```
GET /secure-data HTTP/1.1
Authorization: Digest username="user",
                     realm="example.com",
                     nonce="abc123",
                     uri="/secure-data",
                     *response*="calculated_hash"
```

### 베어러 토큰 (Bearer Token)

베어러 토큰은 **JWT나 OAuth 2.0과 같은 토큰 기반 인증 시스템**에서 사용되는 방식입니다. [(RFC 참고 자료)](https://datatracker.ietf.org/doc/html/rfc6750)

라이언트는 서버로부터 받은 액세스 토큰을 **`Authorization`** 헤더에 포함하여 리소스에 접근 요청을 보냅니다. 토큰은 **`Bearer`** 다음에 공백을 두고 위치하여 보냅니다.

> Bearer”은 소유자라는 뜻인데, “이 토큰의 소유자에게 권한을 부여해줘”라는 의미로 이름을 붙였다고 합니다.
> 
> 
> <img width="770" alt="image" src="https://github.com/user-attachments/assets/2a054b6b-5260-4793-90fd-9832caba3d54" />
> 
> RFC의 Bearer 설명
> 

이런 베어러 토큰을 사용할 때 현재 가장 대중적인 방식이 JWT를 사용하는 방법입니다.
