import socket
import time

class GuessingGameBot:
    def __init__(self, host="127.0.0.1", port=7777):
        self.host = host
        self.port = port
        self.min = 1
        self.max = 100
        
    def play(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print("Connected to the server. Bot will start guessing!")
            
            attempts = 0
            while True:

                guess = (self.min + self.max) // 2
                print(f"Bot guessing: {guess} (range: {self.min}-{self.max})")
                
                # Send the guess to the server
                client_socket.sendall(str(guess).encode())
                response = client_socket.recv(1024).decode()
                print(f"Server response: {response}")
                attempts += 1
                

                if "Correct" in response or "win" in response.lower():
                    print(f"Bot won in {attempts} attempts!")
                    break
                elif "higher" in response.lower() or "too low" in response.lower():
                    self.min = guess + 1
                elif "lower" in response.lower() or "too high" in response.lower():
                    self.max = guess - 1
                else:
                    print(f"Unexpected response: {response}")
                    break
                    
                time.sleep(0.1)
                
                if self.min > self.max:
                    print("Error: Invalid range. Server might be inconsistent.")
                    break

def main():
    bot = GuessingGameBot()
    try:
        bot.play()
    except KeyboardInterrupt:
        print("Stopping bot")
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pass

if __name__ == "__main__":
    main()
