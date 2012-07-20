import Network
import Database.Redis.Command
import Database.Redis.Core

main = do

  resp <- connect localhost 6379  >>= ping
  putStrLn $ show resp
  where
    localhost = "127.0.0.1"
    defaultPort = PortNumber 6379

-- map_keys conn key_map = do
--   map d