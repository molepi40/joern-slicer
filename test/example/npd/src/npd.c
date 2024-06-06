#include <stdio.h>

struct data {
    int flag;
};

static struct data data;

int f(int x)
{
    struct data *p = x ? &data : NULL;

    /* False positive: 'p->flag' is reported as a NULL_DEREFERENCE
     * even though it's protected by the check of 'p', because
     * '&&' evaluates its arguments in order. */
    return (p && p->flag);
}

static void acl_read_cb(int size, void *priv)
{
	struct data *buf = priv;

	if (size > 0) {
		buf->flag += size;
		buf = NULL;
	}
}

static void bluetooth_status_cb(int status)
{

	/* Check the USB status and do needed action if required */
	switch (status) {
	case 1:
		printf("USB device error");
		break;
	case 2:
		printf("USB device reset detected");
		break;
	case 3:
		printf("USB device connected");
		break;
	case 4:
		printf("USB device configured");
		/* Start reading */
		acl_read_cb(0, NULL);
		break;
	case 5:
		printf("USB device disconnected");
		/* Cancel any transfer */
		break;
	case 6:
		printf("USB device suspended");
		break;
	case 7:
		printf("USB device resumed");
		break;
	case 8:
		break;
	case 9:
	default:
		printf("USB unknown state");
		break;
	}
}