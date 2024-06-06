BASE_DIR	:= $(shell pwd)

SRC		:= main.c utils.c

CC		:= gcc
CXX		:= g++
AR		:= ar
CFLAGS		?=
CFLAGS		+= -g -O3 -Wall -Wno-backslash-newline-escape -Wno-pragma-once-outside-header -Wno-writable-strings
ASAN		:= -fsanitize=address
TSAN		:= -fsanitize=thread

all:
	$(CC) $(CFLAGS) $(SRC) -o mytest

clean:
	rm npd