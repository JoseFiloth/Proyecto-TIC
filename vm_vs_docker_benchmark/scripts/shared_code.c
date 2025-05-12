// shared_code.c
void secret_function() {
    volatile int a = 0;
    for (int i = 0; i < 100000; i++) {
        a += i;
    }
}
