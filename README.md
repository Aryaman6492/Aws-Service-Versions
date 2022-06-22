# Aws-Service-Versions
Automated github repository that maintains versions of certain services. Updates everyday.

[![CI Service Versions and Regions](https://github.com/Aryaman6492/Aws-Service-Versions/actions/workflows/main.yml/badge.svg)](https://github.com/Aryaman6492/Aws-Service-Versions/actions/workflows/main.yml)

## List of services that are monitored
1. Redshift clusters latest generation of nodes

        versions.services.red::cluster.node_generation

1. Lambda latest runtime for all environments

        versions.services.lam::function.runtime

1. RDS Instances latest generation of instance classes

        versions.services.rds::instances.classes

1. Fargate Windows Platform Version
    
        versions.services.ecs::fargate_windows.platform_version

1. Fargate Linux Platform Version

        versions.services.ecs::fargate_linux.platform_version

1. Amazon Linux AMI container agent versions
	
        versions.services.ecs::container_amazonlinux.agent_version

1. Amazon Linux 2 AMI container agent versions
	
        versions.services.ecs::container_amazonlinux2.agent_version

1. ElastiCache for Redis versions

        versions.services.ecs::redis.engine_version

1.	ElastiCache for Memcached versions
	
        versions.services.ecs::memcached.engine_version

1. ElastiCache cluster latest node version ( redis )

        versions.services.ecs::redis.node_generation

1.  ElastiCache cluster latest node version ( memcached )
    
        versions.services.ecs::memcached.node_generation

1. EMR Latest generation of instances

        versions.services.emr::instances.versions

1. EMR Latest generation of instances for datapipeline

        versions.services.emr::datapipeline.instances
