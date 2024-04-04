from dependency_injector import providers, containers

from settings.dependency import get_session, get_engine


class IocContainer(containers.DeclarativeContainer):
    # PulPose. 객체생성을 Container에서 관리
    # 1. Repository 에서는 Session에 접근할 수 밖에 없다.
    # 2. Repository 에서 Session을 접근하는 클래스를 Abstract로 만든다.
    # 3. Abstract는 Application 시작과 동시에 IocContainer에서 초기화된다.
    # 4. service, repository에서 session을 사용하는 코드를 제거한다.
    #   4-1 Exception 일어나면 sesssion이 rollback 될 수 있어야 한다.

    session = providers.Singleton(get_session, sa_engine=get_engine)

    loader = providers.AbstractFactory
