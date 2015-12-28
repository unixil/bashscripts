yum groupinstall core -y
yum groupinstall base -y
yum install gcc gcc-c++ binutils make -y
yum update kernel -y
yum install binutils -y
yum install compat-libstdc++-33 -y
yum install compat-libstdc++-33.i686 -y
yum install compat-libcap1 -y
yum install nfs-utils -y
yum install gcc -y
yum install gcc-c++ -y
yum install glibc -y
yum install glibc.i686 -y
yum install glibc-devel -y
yum install glibc-devel.i686 -y
yum install ksh -y
yum install libgcc -y
yum install libgcc.i686 -y
yum install libstdc++ -y
yum install libstdc++.i686 -y
yum install libstdc++-devel -y
yum install libstdc++-devel.i686 -y
yum install libaio -y
yum install libaio.i686 -y
yum install libaio-devel -y
yum install libaio-devel.i686 -y
yum install libXext -y
yum install libXext.i686 -y
yum install libXtst -y
yum install libXtst.i686 -y
yum install libX11 -y
yum install libX11.i686 -y
yum install libXau -y
yum install libXau.i686 -y
yum install libxcb -y
yum install libxcb.i686 -y
yum install libXi -y
yum install libXi.i686 -y
yum install make -y
yum install sysstat -y
yum install unixODBC -y
yum install unixODBC-devel -y
yum install zlib-devel -y
yum install ntp -y
yum install bc -y
yum install perl -y
yum install emacs -y
service ntpd restart
cp /etc/sysctl.conf /etc/sysctl.conf.bakup
echo "vm.swappiness=1">>/etc/sysctl.conf
echo "vm.dirty_background_ratio=3">>/etc/sysctl.conf
echo "vm.dirty_ratio=80">>/etc/sysctl.conf
echo "vm.dirty_expire_centisecs=500">>/etc/sysctl.conf
echo "vm.dirty_writeback_centisecs=100">>/etc/sysctl.conf
pagesize=$(getconf PAGE_SIZE)
echo "kernel.shmmax=4398046511104">>/etc/sysctl.conf
shmall=$(echo "4398046511104/$pagesize"|bc)
echo "kernel.shmall=$shmall">>/etc/sysctl.conf
echo "kernel.shmmni=$pagesize">>/etc/sysctl.conf
echo "kernel.sem=250 32000 100 128">>/etc/sysctl.conf
echo "net.ipv4.ip_local_port_range=9000 65500"
echo "net.core.rmem_default = 262144" >>/etc/sysctl.conf
echo "net.core.rmem_max = 4194304" >>/etc/sysctl.conf
echo "net.core.wmem_default = 262144" >>/etc/sysctl.conf
echo "net.core.wmem_max = 1048576" >>/etc/sysctl.conf
echo "fs.aio-max-nr = 1048576" >>/etc/sysctl.conf
echo "kernel.panic_on_oops=1">>/etc/sysctl.conf
echo "fs.file-max = 6815744" >>/etc/sysctl.conf
sysctl -p
echo "oracle soft nofile 1024" >>/etc/security/limits.conf
echo "oracle hard nofile 65536" >>/etc/security/limits.conf
echo "oracle soft nproc 2047" >>/etc/security/limits.conf
echo "oracle hard nproc 16384" >>/etc/security/limits.conf
echo "oracle soft stack 10240" >>/etc/security/limits.conf
echo "oracle hard stack 32768" >>/etc/security/limits.conf
echo "grid soft nofile 1024" >>/etc/security/limits.conf
echo "grid hard nofile 65536" >>/etc/security/limits.conf
echo "grid soft nproc 2047" >>/etc/security/limits.conf
echo "grid hard nproc 16384" >>/etc/security/limits.conf
echo "grid soft stack 10240" >>/etc/security/limits.conf
echo "grid hard stack 32768" >>/etc/security/limits.conf
##############################################################################
yum -y install gcc make gcc-c++ binutils fuse-libs
yum -y install kernel-uek-devel-`uname -r`
yum -y install kernel-uek-headers-`uname -r`
yum install kernel-uek-devel kernel-uek-headers
yum update kernel
mkdir /media/vmtools
mount /dev/dvdrw /media/vmtools
cd && mkdir vmtools

cp /media/vmtools/* vmtools/ && cd vmtools
tar xvf VMwareTools-10.0.0-2977863.tar.gz

umount /media/vmtools

cd vmware-tools-distrib
#############################################################################
#these are used for oracle linux7 
#cd bin

#sed -i "s/\$content, \$image_file, \$kernRel/\$content,\
#'--builtin=ehci-hcd --builtin=ohci-hcd --builtin=uhci-hcd', \
#\$image_file, \$kernRel/g" \
#vmware-config-tools.pl
##############################################################################
./vmware-install.pl





##############################################################################
groupadd -g 54321 oinstall
groupadd -g 54322 dba
groupadd -g 54323 oper
groupadd -g 54324 backupdba
groupadd -g 54325 dgdba
groupadd -g 54326 kmdba
groupadd -g 54327 asmdba
groupadd -g 54328 asmoper
groupadd -g 54329 asmadmin

sed -i 's/SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config

useradd --uid 54321 --gid oinstall --groups dba,oper,asmdba,asmoper,backupdba,dgdba,kmdba oracle
echo "enter the password for user oracle"
passwd oracle
useradd --uid 54322 --gid oinstall --groups dba,asmadmin,asmdba,asmoper grid
echo "enter the password for user grid"
passwd grid


echo "# Oracle Settings for grid" >> /home/oracle/.bash_profile
echo "export TMP=/tmp" >> /home/oracle/.bash_profile
echo "export TMPDIR=$TMP" >> /home/oracle/.bash_profile
echo "export ORACLE_HOSTNAME=localhost.localdomain" >> /home/oracle/.bash_profile
echo "export ORACLE_UNQNAME=cdb1" >> /home/oracle/.bash_profile
echo "export ORACLE_BASE=/u01/app/oracle" >> /home/oracle/.bash_profile
echo "export ORACLE_HOME=$ORACLE_BASE/product/12.1.0/dbhome_1" >> /home/oracle/.bash_profile
echo "export ORACLE_SID=cdb1" >> /home/oracle/.bash_profile
echo "export PATH=/usr/sbin:$PATH" >> /home/oracle/.bash_profile
echo "export PATH=$ORACLE_HOME/bin:$PATH" >> /home/oracle/.bash_profile
echo "export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib" >> /home/oracle/.bash_profile
echo "export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib" >> /home/oracle/.bash_profile
echo "" >> /home/oracle/.bash_profile

echo "alias sql='sqlplus "/ as sysdba"'" >>/home/oracle/.bash_profile
echo "alias asm=\"sqlplus / as sysasm\"" >>/home/oracle/.bash_profile
echo "alias na=\"cd $ORACLE_HOME/network/admin\"" >>/home/oracle/.bash_profile
echo "alias dbs=\"cd $ORACLE_HOME/dbs\"" >>/home/oracle/.bash_profile
echo "export NLS_DATE_FORMAT='MON-DD-YYYY HH24:MI:SS';" >>/home/oracle/.bash_profile
echo "export PS1='[\u@\h \W]\$ '" >>/home/oracle/.bash_profile
cat<<EOF>>/home/oracle/.bash_profile
if [ $USER = "oracle" ]; then
  if [ $SHELL = "/bin/bash" ]; then
    ulimit -p 16384
    ulimit -n 65536
  else
    ulimit -u 16384 -n 65536
  fi
fi
EOF
echo "" >>/home/oracle/.bash_profile
echo "" >>/home/oracle/.bash_profile
echo "# Oracle Settings for grid" >> /home/grid/.bash_profile
echo "export TMP=/tmp" >> /home/grid/.bash_profile
echo "export TMPDIR=$TMP" >> /home/grid/.bash_profile
echo "export ORACLE_HOSTNAME=localhost.localdomain" >> /home/grid/.bash_profile
echo "export ORACLE_UNQNAME=cdb1" >> /home/grid/.bash_profile
echo "export ORACLE_BASE=/u01/app/grid" >> /home/grid/.bash_profile
echo "export ORACLE_HOME=$ORACLE_BASE/product/12.1.0/grid_1" >> /home/grid/.bash_profile
echo "export ORACLE_SID=cdb1" >> /home/grid/.bash_profile
echo "export PATH=/usr/sbin:$PATH" >> /home/grid/.bash_profile
echo "export PATH=$ORACLE_HOME/bin:$PATH" >> /home/grid/.bash_profile
echo "export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib" >> /home/grid/.bash_profile
echo "export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib" >> /home/grid/.bash_profile
echo "" >> /home/grid/.bash_profile
echo "alias sql='sqlplus "/ as sysdba"'" >>/home/grid/.bash_profile
echo "alias asm='sqlplus "/ as sysasm"'" >>/home/grid/.bash_profile
echo "alias na='cd $ORACLE_HOME/network/admin'" >>/home/grid/.bash_profile
echo "alias dbs='cd $ORACLE_HOME/dbs'" >>/home/grid/.bash_profile
echo "export NLS_DATE_FORMAT='MON-DD-YYYY HH24:MI:SS';" >>/home/grid/.bash_profile
echo "export PS1='[\u@\h \W]\$ '" >>/home/grid/.bash_profile
cat <<EOF>>/home/grid/.bash_profile
if [ $USER = "grid" ]; then
  if [ $SHELL = "/bin/bash" ]; then
    ulimit -u 16384
    ulimit -n 65536
  else
    ulimit -u 16384 -n 65536
  fi
fi
EOF
echo "" >>/home/grid/.bash_profile
echo "" >>/home/grid/.bash_profile
## install oracle grid

mkdir --parents /u01/app/grid
chown --recursive grid.oinstall /u01
chmod --recursive 755 /u01/app/grid

mkdir --parents /u01/app/oracle
chown --recursive oracle.oinstall /u01/app/oracle
chmod --recursive 755 /u01/app/oracle
#################################################
echo " next you need to add asm disk"
echo " fdisk"
tt=$(/sbin/scsi_id -g -u -d /dev/sdb)
echo "KERNEL==\"sd?1\",PROGRAM==\"/sbin/scsi_id -u -g -d /dev/\$parent\",RESULT==\"$tt\",NAME=\"oracleasm/asm-disk1\",OWNER=\"oracle\",GROUP=\"dba\",MODE=\"0660\"">/etc/udev/rules.d/99-oracleasm.rules
echo "about to run start_udev"
start_udev

