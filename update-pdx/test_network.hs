import Data.Maybe (fromJust)
import Database.Redis.ByteStringClass
import Database.Redis.Redis

main = do
    let act r = do (set r "foo" "cool" :: IO (Reply ())) >>= assertRQueued ""
                   (set r "baz" "baz" :: IO (Reply ())) >>= assertRQueued ""

    in do
     redis <- connect localhost defaultPort
     renameCommand redis (toBS "PONG") (toBS "P")
     run_multi r act
     print =<< ping redis
     set redis "hello" "2"
     get redis "hello" >>= fromRBulk' >>=  putStrLn
