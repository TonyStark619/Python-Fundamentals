import time

# Day 20: Decorators - Wrappers for AI pipeline functions

def execution_timer(func):
    """A decorator that measures how long a function takes to execute."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[SYSTEM LOG] '{func.__name__}' finished in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Applying the decorator using the '@' syntax
@execution_timer
def simulate_training_epoch():
    print("Training AI model... processing dataset...")
    # Simulating a heavy computation delay
    time.sleep(1.2)
    print("Epoch 1 Complete.")

print("--- AI Model Diagnostics ---")
simulate_training_epoch()