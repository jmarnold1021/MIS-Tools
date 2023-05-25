USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_CB]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_CB]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_CB]
GO
/****** Object:  Table [dbo].[L56_DOD_CB]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_CB](
	[GI01] [varchar](3) NULL,
	[GI03] [varchar](3) NOT NULL,
	[CB01] [varchar](12) NOT NULL,
	[CB00] [varchar](12) NOT NULL,
	[CB02] [varchar](68) NULL,
	[CB03] [varchar](6) NULL,
	[CB04] [varchar](1) NULL,
	[CB05] [varchar](1) NULL,
	[CB06] [decimal](4, 2) NULL,
	[CB07] [decimal](4, 2) NULL,
	[CB08] [varchar](1) NULL,
	[CB09] [varchar](1) NULL,
	[CB10] [varchar](1) NULL,
	[CB11] [varchar](1) NULL,
	[CB13] [varchar](1) NULL,
	[CB14] [varchar](6) NULL,
	[CB15] [varchar](8) NULL,
	[CB19] [varchar](7) NULL,
	[CB20] [varchar](9) NULL,
	[CB21] [varchar](1) NULL,
	[CB22] [varchar](1) NULL,
	[CB23] [varchar](1) NULL,
	[CB01B] [varchar](12) NULL,
	[CB24] [varchar](1) NULL,
	[CB25] [varchar](1) NULL,
	[CB26] [varchar](1) NULL,
	[CB27] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_CB_GI03_CB00] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CB00] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
