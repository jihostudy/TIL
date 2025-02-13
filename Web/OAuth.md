## OAuth 2.0

OAuth(Open Authentication) 프레임워크는 인터넷 사용자들이 애플리케이션 간에 인증과 권한 부여를 안전하게 공유할 수 있도록 설계된 오픈 표준 프로토콜입니다.

사용자의 비밀번호를 제3자 애플리케이션에 제공하지 않고도, 사용자가 자신의 리소스(예: Google Drive 파일, Facebook 프로필 등)에 대한 접근 권한을 안전하게 부여할 수 있도록 합니다.

<aside>
❓

오픈 표준 프로토콜이란?

**기술 표준이 문서로 공개되어 있어 사용이 자유로운 프로토콜**

</aside>

### 동작 방식

<img width="498" alt="image" src="https://github.com/user-attachments/assets/54303c98-e305-4802-8cae-27e3208215de" />


| 역할 | 설명 | 예시 |
| --- | --- | --- |
| 리소스 소유자 (Resource Owner) | 보통 서비스를 사용하는 최종 사용자 (사람) | 사용자 (User) |
| 클라이언트 (Client) | 사용자 대신 사용자의 데이터에 접근을 요청하는 애플리케이션 | 클라이언트 서버, 백엔드 서버 |
| 인증 서버  | 클라이언트가 사용자의 데이터에 접근할 수 있도록 토큰을 발급하는 서버 | Google, Facebook |
| 리소스 서버 | 사용자의 데이터를 보유하고 있는 서버로, OAuth 2.0을 사용하여 보호됨 | Google, Facebook |

## **OAuth 2.0 동작 순서**

| 단계 | 설명 | 목적 |
| --- | --- | --- |
| 1. 사용자 로그인 요청 | 사용자가 클라이언트 애플리케이션에서 "Login with OAuth Provider" 버튼 클릭 | 사용자에게 로그인 버튼을 제공하기 위해서 |
| 2. 클라이언트가 인증 요청을 인증 서버로 전송 | 클라이언트가 인증 서버 로그인 페이지로 리다이렉트. URL에 `client_id`, `response_type`, `scope`, `redirect_uri` 포함 | 인증 서버가 클라이언트를 식별하고 요청의 유효성을 검증하도록 하기 위해서 |
| 3. 로그인 페이지 제공 | 인증 서버가 사용자에게 로그인 페이지를 제공하여 자격 증명 입력을 요청 | 사용자가 인증 서버에 직접 아이디와 패스워드를 제공하기 위해서 |
| 4. 사용자의 ID/PW 입력 및 제출 | 사용자가 인증 서버 로그인 페이지에서 자격 증명을 입력하고 제출 | - |
| 5. Authorization Code 발급 | 인증 성공 후 인증 서버가 `redirect_uri`에 `authorization_code` 포함하여 리다이렉트 | 클라이언트에 임시 코드를 발급해 액세스 토큰으로 교환할 수 있게 하기 위해서 |
| 6. 클라이언트로의 리다이렉션 | 사용자 브라우저가 `authorization_code`가 포함된 URL을 통해 클라이언트로 리다이렉트 | 인증 서버가 사용자와 클라이언트 간의 상호작용을 연결하는 역할 수행 |
| 7. Authorization Code와 Access Token 교환 | 클라이언트가 `authorization_code`를 인증 서버에 제출해 액세스 토큰 요청 | 클라이언트가 사용자의 데이터에 접근할 권한을 얻기 위해서; 보안을 위해 서버 간 통신 이용 |
| 8. Access Token 발급 | 인증 서버가 액세스 토큰(및 필요시 리프레시 토큰)을 클라이언트에 발급 | 데이터 접근 권한을 부여하는 액세스 토큰을 제공하기 위해서 |
| 9. 로그인 성공 | 클라이언트가 액세스 토큰을 사용해 사용자를 로그인 상태로 설정 | - |
| 10. Access Token으로 리소스 서버에 리소스 요청 | 클라이언트가 액세스 토큰을 사용하여 리소스 서버에 데이터/서비스 요청 | 사용자의 데이터를 접근할 수 있도록 하기 위해서 |
| 11. 리소스 서버의 토큰 검증 | 리소스 서버가 액세스 토큰을 검증함 | 데이터 접근 권한을 확인하기 위해서 |
| 12. 리소스 제공 | 토큰이 유효하면 리소스 서버가 요청된 데이터/서비스를 클라이언트에게 제공 | 사용자에게 필요한 데이터/서비스를 제공하기 위해서 |
| 13. 클라이언트에서 데이터 활용 | 클라이언트가 리소스 서버에서 받은 데이터를 사용해 사용자에게 필요한 기능 제공 | 사용자에게 기능을 제공하기 위해서 |

<aside>
❓

1. Authorization Code를 발급받은 뒤에 6. Redirect URI로 리다이렉트 되는게 무슨 뜻인가요?

Authorization Code은 302 처럼 리다이렉션 Response Code로 되어서, 브라우저에서 자동으로 Redirect URI로 리다이렉션 됩니다.

이때, Authorization Code도 포함해서 백엔드 서버에 넘겨주는 것입니다.

추후, 이 값으로 AT를 요청한다고 생각하시면 됩니다.

</aside>

<aside>
💡

OAuth 1.0 vs OAuth 2.0

OAuth 1.0 에서 OAuth2.0 차이점은 일단 인증 절차 간소화 됨으로써 개발자들이 구현하기 더쉬워졌고, 기존에 사용하던 용어도 바뀌면서 Authorizaiton server와 Resource서버의 분리가 명시적으로 되었다. 

<img width="515" alt="image" src="https://github.com/user-attachments/assets/af17aaa1-fab1-44b9-a53f-1275ff09e58e" />

**인증 절차 간소화**

- 기능의 단순화, 기능과 규모의 확장성 등을 지원하기 위해 만들어 졌다.
- 기존의 OAuth1.0은 디지털 서명 기반이었지만 OAuth2.0의 암호화는 https에 맡김으로써 복잡한 디지털 서명에관한 로직을 요구하지 않기때문에 구현 자체가 개발자입장에서 쉬워짐.

**용어 변경**

- Resource Owner : 사용자 (1.0 User해당)
- Resource Server : REST API 서버 (1.0 Protected Resource)
- Authorization Server : 인증서버 (API 서버와 같을 수도 있음)(1.0 Service Provider)
- Client : 써드파티 어플리케이션 (1.0 Service Provider 해당)

**Resource Server와 Authorization Server서버의 분리**

- 커다란 서비스는 인증 서버를 분리하거나 다중화 할 수 있어야 함.
- Authorization Server의 역할을 명확히 함.

**다양한 인증 방식(Grant_type)**

- Authorization Code Grant
- Implicit Grant
- Resource Owner Password Credentials Grant
- Client Credentials Grant
- Device Code Grant
- Refresh Token Grant
</aside>

### 참고 자료

<aside>
👨‍💻

## RFC란 (feat. OAuth) → 인터넷 표준 문서 (인터넷 기술에 대한 접점)

OAuth 2.0은 인터넷 프로토콜과 보안 표준을 정의하는 RFC(Request for Comments) 문서로 정리되어 있습니다.

특히, OAuth 2.0은 **RFC 6749**에 명시되어 있으며, 사용자와 애플리케이션이 안전하게 데이터를 공유할 수 있도록 인증 및 권한 부여 절차를 정의합니다.

### RFC란?

RFC는 **Request for Comments**의 약자로, 인터넷과 관련된 프로토콜, 절차, 프로그램, 그리고 인터넷 커뮤니티의 기술적 규격을 문서화한 시리즈입니다.

인터넷 기술 표준화 기구인 IETF(Internet Engineering Task Force)에서 발행하며, 인터넷에서 사용되는 기술과 통신 프로토콜의 기준이 되는 중요한 역할을 합니다.

모든 RFC는 IETF의 공개적이고 협력적인 검토를 거쳐 생성됩니다.

### OAuth 2.0과 RFC 6749

OAuth 2.0의 구조와 동작 원리는 **RFC 6749**라는 문서에 상세하게 설명되어 있습니다.

이 문서에서는 OAuth의 **Authorization Code Grant**, **Implicit Grant**, **Resource Owner Password Credentials Grant**, **Client Credentials Grant** 등 네 가지 주요 인증 플로우를 정의하고, 각 단계별 권한 부여와 토큰 처리 절차를 명확히 합니다.

OAuth 2.0의 인증 및 권한 부여 절차가 인터넷에서 표준으로 사용될 수 있도록 RFC 6749 문서는 다음을 목표로 작성되었습니다.

| 목표 | 내용 |
| --- | --- |
| 보안성 강화 | 사용자 인증 정보를 직접 노출하지 않고도 애플리케이션이 사용자 데이터를 접근할 수 있게 합니다. |
| 확장성 보장 | 다양한 애플리케이션과 서비스에 맞게 확장 가능한 구조를 제공합니다. |
| 개발자 편의성 증대 | 클라이언트 애플리케이션이 최소한의 노력으로 인증 절차를 구현할 수 있게 합니다. |
</aside>

<aside>
❓ RFC는 왜 중요한가요??

</aside>

<aside>
👨‍💻

RFC는 모든 인터넷 표준의 **공식적인 규격서** 역할을 합니다.

누구나 RFC 문서를 통해 인터넷에서 사용되는 프로토콜을 확인하고, 준수할 수 있어, 서비스 간 상호 운용성(interoperability)을 높입니다.

OAuth 2.0을 포함한 여러 인터넷 표준이 RFC로 정의되어 있기 때문에, 이를 참고함으로써 **일관성 있는 보안 구현과 서비스 연결**을 쉽게 수행할 수 있습니다.

</aside>

### 내가 가졌던 의문

<aside>
❓

Redirect URL로 리다이렉트되는 이유가 무엇일까?

OAuth 제공자는 사전에 등록된 Callback URL만 허용해서, 이를 통해 악의적인 사이트로 Authorization Code가 전달되는 걸 방지합니다.

</aside>

<aside>
❓

OAuth는 네트워크 헤드에 값을 넣는 방법들이 아닌, 일종의 인증/인가 로직으로 보이는데 맞나요? (네트워크 단에서 제공해야 하는 필드들은 기존의 Authorization을 사용하는 것이구요)

네

OAuth는 인증 프레임워크로, 인증과 권한 부여를 위한 방법이라고 이해하시면 됩니다.

</aside>
