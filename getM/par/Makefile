CC = gcc
CFLAGS = -W -Wall
TARGET = par
OBJECTS = par.o

all:$(TARGET)
$(TARGET) : $(OBJECTS)
	$(CC) -o $@ $^
clean :
	rm  *.o $(TARGET)
