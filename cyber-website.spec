Name:		cyber-website
# 1.0.<Build>
Version:	%{!?version:1.0.0}%{?version}
# ${commit_count}_${git_commit}
Release:	%{!?release:1}%{?release}
Summary:	Cyberlife Website

Group:		Application
License:	GPL
URL:		http://www.cyber-life.cn/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python(abi) = 2.7
Requires:	systemd python(abi) = 2.7 nginx

%undefine __check_files

%description

%prep

%build
make

%install
make install DESTDIR=%{buildroot}

%post
/usr/bin/systemctl daemon-reload

/usr/bin/systemctl enable mariadb.service
/usr/bin/systemctl start mariadb.service

count=0
max=3

while ! ls /var/lib/mysql/mysql.sock && [ $count -lt $max ]
do
        sleep 1
        ((++count))
done

mysql -u root 2>&1 < /opt/cyberlife/service/cyber-website/create_table.sql | tee /root/cyber-website.rpm.post.log

for default_config in /etc/cyberlife/*website*.default
do
        config=${default_config%.default}
        if [ ! -f $config ]; then
                cp $default_config $config
        fi
done

for default_config in /etc/cyberlife/*ssdb-article*.default
do
        config=${default_config%.default}
        if [ ! -f $config ]; then
                cp $default_config $config
        fi
done

mkdir -p /opt/cyberlife/logs
mkdir -p /opt/cyberlife/data/ssdb-article

systemctl enable cyber-ssdb-article.service
systemctl restart cyber-ssdb-article.service
systemctl enable cyber-website.service
systemctl restart cyber-website.service
systemctl enable cyber-website-swagger.service
systemctl restart cyber-website-swagger.service
systemctl enable nginx.service
systemctl restart nginx.service

%postun
/usr/bin/systemctl daemon-reload

%files
/etc/cyberlife/*
/etc/nginx/location.d/*
/etc/nginx/conf.d/*
/opt/cyberlife/service/cyber-website/*
/etc/systemd/system/*

%doc

%changelog
