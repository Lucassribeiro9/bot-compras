# mudando para aws
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.13.0"
    }
  }
}

provider "aws" {
  # Configuração do provedor AWS
  region = "us-east-1"
}
# ----- Criando VPC -----
resource "aws_vpc" "bot_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "bot_vpc"
    Description = "VPC para a infra do bot"
  }
}
resource "aws_subnet" "bot_subnet" {
  vpc_id            = aws_vpc.bot_vpc.id
  cidr_block        = "10.0.1.0/24"
  tags = {
    Name = "bot_subnet"
    Description = "Subnet para a infra do bot"
  }
}
resource "aws_internet_gateway" "bot_igw" {
  vpc_id = aws_vpc.bot_vpc.id
  tags = {
    Name = "bot_igw"
    Description = "Internet Gateway para a infra do bot"
  }
}
resource "aws_route_table" "bot_route_table" {
  vpc_id = aws_vpc.bot_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.bot_igw.id
  }
  tags = {
    Name = "bot_route_table"
    Description = "Route Table para a infra do bot"
  }
}
resource "aws_route_table_association" "bot_route_table_association" {
  subnet_id      = aws_subnet.bot_subnet.id
  route_table_id = aws_route_table.bot_route_table.id
}
resource "aws_security_group" "bot_sg" {
  vpc_id = aws_vpc.bot_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "bot_sg"
    Description = "Security Group para a infra do bot"
  }
}
# ----- Criando Key Pair -----
resource "aws_key_pair" "bot_key_pair" {
  key_name   = "bot_key_pair"
  public_key = file("~/.ssh/id_rsa.pub") # Caminho para a sua chave pública
}
# ----- Criando EC2 -----
resource "aws_instance" "bot_ec2" {
  ami           = "ami-0360c520857e3138f" # Amazon Linux 2 AMI (HVM), SSD Volume Type
  instance_type = "t3.micro"
  key_name      = aws_key_pair.bot_key_pair.key_name
  subnet_id     = aws_subnet.bot_subnet.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.bot_sg.id]
  user_data = <<-EOF
              #!/bin/bash
              # Atualizar sistema
              sudo yum update -y
              
              # Instalar Docker
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              
              # Instalar Docker Compose
              sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              
              # Instalar Git
              sudo yum install git -y
              EOF
  tags = {
    Name = "bot_ec2"
    Description = "Instância EC2 para rodar o bot"
  }
}