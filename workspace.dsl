workspace {
    name "Магазин"
    description "Система для управления магазином с товарами и корзиной покупателя"

    !identifiers hierarchical

    model {
        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь" {
            description "Пользователь магазина"
        }

        shop_system = softwareSystem "Система магазина" {
            description "Система для управления магазином"

            user_service = container "User Service" {
                description "Сервис для управления пользователями"
                technology "REST API"
            }

            product_service = container "Product Service" {
                description "Сервис для управления товарами"
                technology "REST API"
            }

            cart_service = container "Cart Service" {
                description "Сервис для управления корзиной"
                technology "REST API"
            }

            group "Слой данных" {
                postgres_database = container "PostgreSQL Database" {
                    description "База данных PostgreSQL с информацией о пользователях, товарах и корзинах"
                    technology "PostgreSQL"
                    tags "database"
                }

                redis_cache = container "Redis Cache" {
                    description "Кеш Redis для ускорения авторизации"
                    technology "Redis"
                    tags "cache"
                }
                    
                mongo_database = container "MongoDB Database" {
                    description "База данных MongoDB со всеми товарами"
                    technology "MongoDB"
                    tags "database"
                }
            }

            user -> user_service "Работа с пользователями"
            user -> cart_service "Добавление товара в корзину, получение корзины для пользователя"
            user -> product_service "Получение списка товаров"

            user_service -> postgres_database "CRUD операции с пользователями"
            product_service -> postgres_database "CRUD операции с товарами"
            cart_service -> postgres_database "CRUD операции с корзинами"

            user_service -> redis_cache "Быстрая авторизация пользователей"
            cart_service -> postgres_database "Связывание товаров с корзинами"
            cart_service -> product_service "Для поиска товаров в корзине"
            cart_service -> mongo_database "Получить корзину пользователя"
            product_service -> mongo_database "Сохранить данные товара"
        }
    }


    views {
        themes default

        properties { 
            structurizr.tooltips true
        }

        !script groovy {
            workspace.views.createDefaultViews()
            workspace.views.views.findAll { it instanceof com.structurizr.view.ModelView }.each { it.enableAutomaticLayout() }
        }

        dynamic shop_system "UC01" "Создание нового пользователя" {
            autoLayout
            user -> shop_system.user_service "Создать нового пользователя (POST /users)"
            shop_system.user_service -> shop_system.postgres_database "Сохранить данные пользователя"
            shop_system.user_service -> shop_system.redis_cache "Кэшировать данные о пользователе"
        }

        dynamic shop_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> shop_system.user_service "Поиск пользователя (GET /users/{login})"
            shop_system.user_service -> shop_system.redis_cache "Проверить кэш пользователя"
            shop_system.user_service -> shop_system.postgres_database "Получить данные о пользователе"
        }

        dynamic shop_system "UC03" "Поиск пользователя по маске имени и фамилии" {
            autoLayout
            user -> shop_system.user_service "Поиск пользователя (GET /users?name={name})"
            shop_system.user_service -> shop_system.postgres_database "Получить данные пользователя"
        }

        dynamic shop_system "UC04" "Создание товара" {
            autoLayout
            user -> shop_system.product_service "Создать товар (POST /products)"
            shop_system.product_service -> shop_system.mongo_database "Сохранить данные товара"
        }

        dynamic shop_system "UC05" "Получение списка товаров" {
            autoLayout
            user -> shop_system.product_service "Получить список товаров (GET /products)"
            shop_system.product_service -> shop_system.mongo_database "Получить данные всех товаров"
        }

        dynamic shop_system "UC06" "Добавление товара в корзину" {
            autoLayout
            user -> shop_system.cart_service "Добавить товар в корзину (POST /cart/{user_id}/add/{product_id})"
            shop_system.cart_service -> shop_system.postgres_database "Добавить товар в корзину пользователя"
        }

        dynamic shop_system "UC07" "Получение корзины для пользователя" {
            autoLayout
            user -> shop_system.cart_service "Получить корзину пользователя (GET /cart/{user_id})"
            shop_system.cart_service -> shop_system.mongo_database "Получить корзину пользователя"
        }

        dynamic shop_system "UC08" "Получение списка товаров в корзине" {
            autoLayout
            user -> shop_system.cart_service "Получить список товаров в корзине (GET /cart/{user_id}/products)"
            shop_system.cart_service -> shop_system.postgres_database "Получить список товаров в корзине пользователя"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}
