USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_XE]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_XE]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_XE]
GO
/****** Object:  Table [dbo].[L56_DOD_XE]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_XE](
	[GI01] [varchar](3) NULL,
	[GI03] [varchar](3) NOT NULL,
	[CB01] [varchar](12) NOT NULL,
	[XB00] [varchar](6) NOT NULL,
	[CB00] [varchar](12) NOT NULL,
	[XF00] [varchar](2) NOT NULL,
	[EB00] [varchar](9) NOT NULL,
	[XE01] [varchar](1) NOT NULL,
	[XE02] [int] NULL,
	[XE03] [decimal](5, 2) NULL,
	[XE04] [decimal](5, 2) NULL,
 CONSTRAINT [PK_DOD_XE_GI03_CB00_XB00_XF00_EB00_XE01] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CB00] ASC,
	[XB00] ASC,
	[XF00] ASC,
	[EB00] ASC,
	[XE01] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
