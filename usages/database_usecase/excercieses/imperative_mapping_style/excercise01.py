from usages.database_usecase._initialize.imperative_mapped_setup import start_mapper

from usages.database_usecase.config.client import get_session, get_engine

from usages.database_usecase.excercieses.imperative_mapping_style.entities import MemberEntity


def execute_imperative_lazy_joind(engine):
    """ imperatively mapping의 lazy가 'joined' 으로 설정된 경우
    ```python
        properties={
            'profile': relationship(
                MemberProfileEntity,
                primaryjoin=(
                        Member.nanoid == foreign(MemberProfile.nanoid)
                ),
                lazy='joined',
                uselist=True
            )
        }
    ```
    Desc:
        - "lazy"가 joined으로 설정된 경우 query가 Left join이 적용되어 실행된다.
        - 어떤 객체를 조회할때 아무런 기본적으로 로딩될 데이터에 대해서 설정하는 경우 사용한다.
        - 이 경우엔 추가 쿼리가 발생하지 않는다.
    Usage:
        ```
        query = session.query(MemberEntity) \
        .filter(MemberEntity.nanoid == 'U3M065V1XtRa') \
        .one_or_none()

        print(query.profile)
        ```
    """
    session = get_session(engine)
    query = session.query(MemberEntity) \
        .filter(MemberEntity.nanoid == 'U3M065V1XtRa') \
        .one_or_none()
    print(query.profile)

    session.commit()

    session.close()


def execute_imperative_lazy_select(engine):
    """ imperatively mapping의 lazy가 'select' 으로 설정된 경우
    ```python
        properties={
            'profile': relationship(
                MemberProfileEntity,
                primaryjoin=(
                        Member.nanoid == foreign(MemberProfile.nanoid)
                ),
                lazy='select',
                uselist=True
            )
        }
    ```
    Desc:
         - "lazy"가 select으로 설정된 경우 query는 Left join이 적용되지 않는다.
         -  필요 속성에 접근하는 경우, 추가 쿼리가 발생한다.

    Usage:
        - 아래의 경우 추가 쿼리는 발생하지 않는다.
            ```
            query = session.query(MemberEntity) \
            .filter(MemberEntity.nanoid == 'U3M065V1XtRa') \
            .one_or_none()
            ```
        - 아래의 경우 추가 쿼리가 발생한다.
            ```
            query = session.query(MemberEntity) \
            .filter(MemberEntity.nanoid == 'U3M065V1XtRa') \
            .one_or_none()
            print(query.profile)
            ```

    Note:
        - 이 옵션은 필요 속성을 선택적으로 접근하는 경우에 사용하면 유용하다. "joined"의 경우 조회시 기본적으로 모든 값을 들고오는 반면
          이 옵션은 속성에 접근하기 전까지 쿼리가 추가적으로 발생하지 않는다.

    """
    session = get_session(engine)
    query = session.query(MemberEntity).limit(10).all()

    for row in query:
        print(row, row.profile)

    session.commit()

    session.close()


if __name__ == '__main__':
    start_mapper(lazy_option="raise")

    engine = get_engine()

    execute_imperative_lazy_select(engine)

    engine.dispose()
