#include <stdio.h>                                                                                                                    
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <regex.h>

#define IP_PROTOCOL 0

void p_error(char* msg) {
  fprintf(stderr, "\n\033[1;31m[E] \033[1;37m%s\033[0m\n", msg);
}

void p_info(char* msg) {
  fprintf(stdout, "\n\033[1;36m[I] \033[1;37m%s\033[0m\n", msg);
}

void p_success(char* msg) {
  fprintf(stdout, "\n\033[1;32m[S] \033[1;37m%s\033[0m\n", msg);
}

void p_success_int(int n) {
  fprintf(stdout, "\033[1;32m[S] \033[1;37m%i\033[0m\n", n);
}

void progress_bar(int progress, int total, int barWidth) {
  float progressRatio = (float)progress / total;
  int numChars = progressRatio * barWidth;

  printf("[");
  for (int i = 0; i < barWidth; ++i) {
    if (i < numChars) {
      printf("=");
    } else {
      printf(" ");
    }
  }
  printf("] %d%%\r", (int)(progressRatio * 100));
  fflush(stdout); // limpar o buffer de saída
}

int is_valid_ipv4(char* ip) {
  regex_t regex;
  int reti;
  char pattern[] = "^([1-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.([1-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

  reti = regcomp(&regex, pattern, REG_EXTENDED);

  if (reti) {
    p_error("Could not compile regex");
    return 0;
  }

  reti = regexec(&regex, ip, 0, NULL, 0);

  if (reti == 0) return 1;

  return 0;
}

int test_port(char* ip, int port) {
  int sock;
  int conn;

  struct sockaddr_in target;
  struct timeval timeout;

  timeout.tv_sec = 5;
  timeout.tv_usec = 0;

  sock = socket(AF_INET, SOCK_STREAM, IP_PROTOCOL);

  if (setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (char*)&timeout, sizeof(timeout)) < 0) {
    p_error("Could not set timeout");
    exit(1);
  }

  target.sin_family = AF_INET;
  target.sin_port = htons(port);
  target.sin_addr.s_addr = inet_addr(ip);

  conn = connect(sock, (struct sockaddr*)&target, sizeof(target));

  if (conn == 0) {
    close(sock);
    close(conn);
  }

  return conn;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    p_error("Missing host argument");
    exit(1);
  }

  char* ip = argv[1];

  if (is_valid_ipv4(ip) == 0) {
    p_error("Invalid ip address");
    exit(1);
  }

  int top_ports[] = {
    0,1,5,7,9,11,13,17,18,19,20,21,22,23,25,26,35,37,38,39,41,42,43,49,53,57,67,68,69,
    70,79,80,81,82,88,101,102,107,109,110,111,113,115,117,118,119,123,135,137,138,139,
    143,152,153,156,158,161,162,170,179,194,201,209,213,218,220,259,264,311,318,323,366,
    369,371,383,384,387,389,401,411,412,427,443,444,445,464,465,500,502,512,513,514,515,
    517,518,520,524,525,530,531,532,533,540,542,543,544,546,547,548,550,554,556,560,561,
    563,587,591,593,604,631,636,639,646,647,648,652,654,665,666,674,691,692,694,695,698,
    699,700,701,702,706,711,712,720,749,750,782,829,860,873,901,902,904,911,981,989,990,
    991,992,993,995,1059,1080,1099,1109,1167,1176,1182,1194,1198,1200,1214,1223,1234,1241,
    1248,1270,1311,1313,1337,1344,1352,1387,1414,1431,1433,1434,1494,1512,1514,1521,1522,
    1524,1526,1533,1547,1550,1581,1589,1627,1677,1701,1716,1723,1725,1755,1761,1762,1812,
    1813,1863,1883,1900,1935,1965,1970,1971,1972,1975,1984,1985,2000,2002,2030,2031,2049,
    2053,2056,2074,2082,2083,2086,2087,2095,2096,2161,2181,2200,2219,2220,2222,2301,2302,
    2303,2305,2369,2370,2381,2400,2404,2427,2447,2483,2484,2546,2593,2598,2612,2710,2735,
    2809,2944,2945,2948,2949,2967,3000,3001,3002,3003,3004,3006,3007,3050,3074,3128,3260,
    3305,3306,3333,3389,3396,3689,3690,3784,3785,3872,3900,3945,4000,4007,4089,4093,4096,
    4100,4111,4224,4226,4569,4662,4664,4672,4894,4899,5000,5001,5003,5004,5005,5050,5051,
    5060,5061,5093,5104,5121,5190,5222,5223,5269,5351,5353,5402,5405,5432,5445,5495,5498,
    5499,5500,5501,5517,5555,5556,5631,5666,5667,5800,5814,5900,5938,6000,6001,6005,6050,
    6051,6112,6129,6257,6346,6347,6502,6522,6543,6566,6619,6665,6679,6697,6699,6881,6891,
    6901,6969,7000,7001,7002,7005,7006,7010,7171,7312,7659,7707,7777,8000,8002,8008,8010,
    8074,8080,8086,8087,8090,8118,8200,8220,8222,8291,8294,8330,8331,8332,8333,8400,8443,
    8500,8767,8880,8888,9000,9001,9009,9043,9060,9100,9101,9102,9103,9200,9535,9800,9999,
    10000,10001,10008,10050,10051,10113,10114,10115,10116,10480,11235,11294,11371,11576,
    12345,12975,13720,13721,13724,13782,13783,14567,15000,15345,15567,16384,16567,19226,
    19813,20000,20720,22347,22350,24800,24842,25565,25575,25999,26000,27000,27010,27015,
    27374,27500,27888,27900,27901,27960,28910,28960,29900,29920,30000,30564,31337,31415,
    31456,32245,32400,33434,36963,37777,40000,43594,47808
  };

  size_t total_ports = sizeof(top_ports) / sizeof(int);

  int found_ports[total_ports];
  int found_ports_n = 0;

  p_info("Scanning top ports\n");

  for (size_t i = 0; i < total_ports; i++) {
    int port = top_ports[i];
    int result = test_port(ip, port);

    if (result == 0) {
      found_ports[found_ports_n] = port;
      found_ports_n++;
    }

    progress_bar(i, total_ports - 1, 50);
  }

  printf("\n");
  p_info("PORTS FOUND:\n");

  for (size_t i = 0; i < found_ports_n; i++) {
    int port = found_ports[i];

    p_success_int(port);
  }
}
