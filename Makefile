CC = gcc
CFLAGS = -W -Wall
TARGET = comPtn
OBJECTS = comPtn.o

all:$(TARGET)
$(TARGET) : $(OBJECTS)
	$(CC) -o $@ $^
clean :
	rm  *.o $(TARGET)
