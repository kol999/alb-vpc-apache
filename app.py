#!/usr/bin/env python3
import base64
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)


class LoadBalancerStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        vpc = ec2.Vpc(self, "DemoVPC")

        data_blue = open("./httpd-blue.sh", "rb").read()
        httpd_blue = ec2.UserData.for_linux()
        httpd_blue.add_commands(str(data_blue, 'utf-8'))

        asg_blue = autoscaling.AutoScalingGroup(
            self,
            "ASG-Blue",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=httpd_blue,
        )

        data_green = open("./httpd-green.sh", "rb").read()
        httpd_green = ec2.UserData.for_linux()
        httpd_green.add_commands(str(data_green, 'utf-8'))

        asg_green = autoscaling.AutoScalingGroup(
            self,
            "ASG-Green",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=httpd_green,
        )

        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True)

        listener = lb.add_listener("Listener", port=80)
        listener.add_targets("Target", port=80, targets=[asg_blue])
        listener.connections.allow_default_port_from_any_ipv4(
            "Open to the world")

        asg_blue.scale_on_request_count(
            "AModestLoad", target_requests_per_second=1)
        core.CfnOutput(self, "LoadBalancer", export_name="LoadBalancer",
                       value=lb.load_balancer_dns_name)


app = core.App()
LoadBalancerStack(app, "LoadBalancerStack")
app.synth()
