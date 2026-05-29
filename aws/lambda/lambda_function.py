import json
import boto3
import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2', region_name='eu-central-1')

def lambda_handler(event, context):
    try:
        logger.info(f"Otrzymano zdarzenie z Wazuha: {json.dumps(event)}")
        body = json.loads(event.get('body', '{}'))
        
        data_fields = body.get('data', {})
        aws_fields = data_fields.get('aws', {})
        
        src_ip = aws_fields.get('srcaddr') or data_fields.get('srcip') or body.get('srcip')
        
        if not src_ip:
            logger.error("Nie udalo sie wyciagnac adresu IP z otrzymanego alertu.")
            return {
                'statusCode': 400,
                'body': json.dumps('Blad: Brak IP atakujacego w strukturze JSON.')
            }
            
        logger.info(f"Identyfikacja napastnika zakonczona sukcesem. IP: {src_ip}")
        
        NACL_ID = 'acl-xxxxxxxxxxxxxxxxx'  # Placeholder for Network ACL ID
        
        rule_number = random.randint(100, 32000) 
        
        response = ec2.create_network_acl_entry(
            NetworkAclId=NACL_ID,
            RuleNumber=rule_number,
            Protocol='-1',          
            RuleAction='deny',      
            Egress=False,           
            CidrBlock=f"{src_ip}/32" 
        )
        
        logger.info(f"SUKCES: Adres IP {src_ip} zostal zablokowany na poziomie sieciowym w NACL {NACL_ID}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Incident Response zakonczony sukcesem. Zablokowano: {src_ip}")
        }
        
    except Exception as e:
        logger.error(f"Blad podczas realizacji procedury Incident Response: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Blad wewnetrzny Lambda: {str(e)}")
        }
